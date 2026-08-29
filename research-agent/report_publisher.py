"""Publish research agent output as linkable GitHub Pages HTML + JSON."""

from __future__ import annotations

import html
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from issue_taxonomy import (
    AUDIENCE_ORDER,
    build_grouped_summary,
    classify_product_area,
    group_by_audience_and_theme,
    tag_issues,
    tag_research_items,
)
from affinity_board import (
    build_affinity_cards,
    designops_assets_hrefs,
    designops_auth_gate_html,
    designops_auth_head_scripts,
    designops_theme_boot_script,
    github_actions_workflow_url,
    group_affinity_board,
    render_affinity_board_html,
    report_nav_html,
    report_nav_hrefs,
)
from voice_of_user import (
    SIGNAL_LABELS,
    classify_feedback_item,
    classify_listing_signal,
    collect_user_report_cards,
    is_dovetail_user_voice,
    is_outset_user_voice,
)

DOCS_ROOT = Path(os.environ.get("REPORT_OUTPUT_DIR", "docs/research"))
GITHUB_PAGES_URL = os.environ.get("GITHUB_PAGES_URL", "").rstrip("/")
REPORT_MAX_RESEARCH_ITEMS = int(os.environ.get("REPORT_MAX_RESEARCH_ITEMS", "100"))

SOURCE_ORDER = ("posthog", "pendo", "dovetail", "freshdesk", "outset")
SOURCE_LABELS = {
    "posthog": "PostHog",
    "pendo": "Pendo",
    "dovetail": "Dovetail",
    "freshdesk": "Freshdesk",
    "outset": "Outset",
}


def _esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def _severity_badge(severity: str) -> str:
    color = "#d32f2f" if severity == "HIGH" else "#f57c00"
    return f'<span class="badge" style="background:{color}">{_esc(severity)}</span>'


def _research_item_attrs(source: str, audience: str = "", theme: str = "") -> str:
    return (
        f'class="verified filterable" data-source="{_esc(source)}" '
        f'data-audience="{_esc(audience)}" data-theme="{_esc(theme)}"'
    )


def _render_research_list(context: Dict[str, Any]) -> str:
    items: List[str] = []

    for item in context.get("pendo_feedback", []):
        attrs = _research_item_attrs("pendo", item.get("audience", ""), item.get("theme", ""))
        items.append(
            f'<li {attrs}><strong>Pendo</strong> ({_esc(item.get("guide_name", "Guide"))}): '
            f'"{_esc(item.get("response", ""))}"</li>'
        )

    for item in context.get("dovetail_insights", []):
        title = _esc(item.get("title", "Untitled"))
        link = item.get("url")
        attrs = _research_item_attrs("dovetail", item.get("audience", ""), item.get("theme", ""))
        if link:
            items.append(f'<li {attrs}><strong>Dovetail</strong>: <a href="{_esc(link)}">{title}</a></li>')
        else:
            items.append(f'<li {attrs}><strong>Dovetail</strong>: {title}</li>')

    for item in context.get("freshdesk_tickets", []):
        subject = _esc(item.get("subject", "Support ticket"))
        body_preview = _esc((item.get("body") or "")[:240])
        link = item.get("url")
        meta = _esc(item.get("ticket_type") or item.get("status") or "Freshdesk")
        attrs = _research_item_attrs("freshdesk", item.get("audience", ""), item.get("theme", ""))
        if link:
            items.append(
                f'<li {attrs}><strong>Freshdesk</strong> ({meta}): '
                f'<a href="{_esc(link)}">{subject}</a><br/><em>{body_preview}</em></li>'
            )
        else:
            items.append(
                f'<li {attrs}><strong>Freshdesk</strong> ({meta}): {subject}<br/><em>{body_preview}</em></li>'
            )

    for item in context.get("outset_studies", []):
        title = _esc(item.get("title", "Untitled"))
        link = item.get("url")
        attrs = _research_item_attrs("outset", item.get("audience", ""), item.get("theme", ""))
        if link:
            items.append(f'<li {attrs}><strong>Outset</strong>: <a href="{_esc(link)}">{title}</a></li>')
        else:
            items.append(f'<li {attrs}><strong>Outset</strong>: {title}</li>')

    if not items:
        return "<li>No related qualitative research found.</li>"
    return "\n".join(items)


def build_report_payload(
    *,
    week_start: str,
    posthog_dropoffs: List[Dict[str, Any]],
    synthesis: Dict[str, str],
    pendo_feedback: List[Dict[str, Any]],
    dovetail_insights: List[Dict[str, Any]],
    freshdesk_tickets: List[Dict[str, Any]],
    outset_studies: List[Dict[str, Any]],
    pendo_analytics: Optional[List[Dict[str, Any]]] = None,
    top_issues_limit: int = 20,
    lookback_days: int = 90,
) -> Dict[str, Any]:
    tagged_issues = posthog_dropoffs
    grouped_issues = group_by_audience_and_theme(tagged_issues)
    audience_summary = build_grouped_summary(grouped_issues)

    tagged_pendo = tag_research_items(pendo_feedback)
    tagged_pendo_analytics = tag_research_items(pendo_analytics or [])
    tagged_dovetail = tag_research_items(dovetail_insights)
    tagged_freshdesk = tag_research_items(freshdesk_tickets)
    tagged_outset = tag_research_items(outset_studies)

    high = len([i for i in tagged_issues if i.get("severity") == "HIGH"])
    medium = len([i for i in tagged_issues if i.get("severity") == "MEDIUM"])
    enriched = len([
        i for i in tagged_issues
        if any(i.get("research_context", {}).get(key) for key in (
            "pendo_feedback", "dovetail_insights", "freshdesk_tickets", "outset_studies"
        ))
    ])
    synthesized = len([t for t in synthesis if synthesis.get(t)])
    pendo_total = len(pendo_feedback) + len(pendo_analytics or [])

    period_end = datetime.utcnow().date()
    period_start = period_end - timedelta(days=lookback_days)
    source_counts = {
        "posthog": len(tagged_issues),
        "pendo": pendo_total,
        "dovetail": len(dovetail_insights),
        "freshdesk": len(freshdesk_tickets),
        "outset": len(outset_studies),
    }
    max_items = REPORT_MAX_RESEARCH_ITEMS

    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "week_start": week_start,
        "period": {
            "lookback_days": lookback_days,
            "label": "Last 3 months" if lookback_days >= 90 else f"Last {lookback_days} days",
            "start": period_start.isoformat(),
            "end": period_end.isoformat(),
        },
        "source_counts": source_counts,
        "summary": {
            "issues_found": len(tagged_issues),
            "issues_reported": len(tagged_issues),
            "top_issues_limit": top_issues_limit,
            "ai_synthesized_count": synthesized,
            "high_severity": high,
            "medium_severity": medium,
            "issues_with_research_context": enriched,
            "pendo_feedback_count": len(pendo_feedback),
            "pendo_analytics_count": len(pendo_analytics or []),
            "dovetail_insights_count": len(dovetail_insights),
            "freshdesk_tickets_count": len(freshdesk_tickets),
            "outset_studies_count": len(outset_studies),
            "by_audience": audience_summary,
        },
        "sources": {
            "posthog": bool(tagged_issues),
            "pendo": bool(pendo_total),
            "dovetail": bool(dovetail_insights),
            "freshdesk": bool(freshdesk_tickets),
            "outset": bool(outset_studies),
        },
        "posthog_dropoffs": tagged_issues,
        "issues": tagged_issues,
        "grouped_issues": grouped_issues,
        "synthesis": synthesis,
        "pendo_feedback": tagged_pendo[:max_items],
        "pendo_analytics": tagged_pendo_analytics,
        "dovetail_insights": tagged_dovetail,
        "freshdesk_tickets": tagged_freshdesk[:max_items],
        "outset_studies": tagged_outset[:max_items],
    }


def _render_issue_card(issue: Dict[str, Any], synthesis: Dict[str, str]) -> str:
    title = issue.get("title", "Untitled issue")
    analysis = synthesis.get(title, "Analysis pending.")
    context = issue.get("research_context", {})
    theme = issue.get("theme", "")
    audience = issue.get("audience", "")
    meta = ""
    if audience or theme:
        meta = (
            f'<p class="taxonomy">'
            f'<span class="pill audience">{_esc(audience)}</span> '
            f'<span class="pill theme">{_esc(theme)}</span>'
            f"</p>"
        )

    return f"""
            <article class="issue-card filterable"
              data-source="posthog"
              data-audience="{_esc(audience)}"
              data-theme="{_esc(theme)}"
              data-severity="{_esc(issue.get('severity', 'MEDIUM'))}">
              <header>
                <h3>{_esc(title)}</h3>
                {_severity_badge(issue.get("severity", "MEDIUM"))}
              </header>
              {meta}
              <div class="metrics">
                <span><strong>Drop-off:</strong> {issue.get("drop_percentage", 0)}%</span>
                <span><strong>Users:</strong> {issue.get("users_affected", 0)}</span>
                <span><strong>Funnel:</strong> {_esc(issue.get("funnel_name", ""))}</span>
              </div>
              <p class="step"><strong>Step:</strong> {_esc(issue.get("step", ""))}</p>
              <div class="analysis ai-generated">
                <h4>AI analysis</h4>
                <p>{_esc(analysis)}</p>
              </div>
              <div class="research">
                <h4>Related research</h4>
                <ul>{_render_research_list(context)}</ul>
              </div>
              <p class="links"><a href="{_esc(issue.get("posthog_link", "#"))}">View in PostHog</a></p>
            </article>
            """


def _render_issue_cards(issues: List[Dict[str, Any]], synthesis: Dict[str, str]) -> str:
    if not issues:
        return '<p class="empty">No significant funnel drop-offs detected in this period.</p>'
    return "\n".join(_render_issue_card(issue, synthesis) for issue in issues)


def _render_grouped_issues(
    grouped: Dict[str, Dict[str, List[Dict[str, Any]]]],
    synthesis: Dict[str, str],
) -> str:
    if not any(grouped.get(a) for a in AUDIENCE_ORDER):
        return '<p class="empty">No significant funnel drop-offs detected in this period.</p>'

    sections: List[str] = []
    for audience in AUDIENCE_ORDER:
        themes = grouped.get(audience, {})
        if not themes:
            continue

        theme_blocks: List[str] = []
        for theme in sorted(themes.keys()):
            items = themes[theme]
            cards = "\n".join(_render_issue_card(issue, synthesis) for issue in items)
            theme_blocks.append(
                f'<section class="theme-section" data-audience="{_esc(audience)}" data-theme="{_esc(theme)}">'
                f'<h3>{_esc(theme)} <span class="count">({len(items)})</span></h3>'
                f"{cards}"
                f"</section>"
            )

        issue_count = sum(len(items) for items in themes.values())
        sections.append(
            f'<section class="audience-section" data-audience="{_esc(audience)}">'
            f'<h2>{_esc(audience)} <span class="count">({issue_count} issues)</span></h2>'
            f'{"".join(theme_blocks)}'
            f"</section>"
        )

    return "\n".join(sections)


def _render_grouped_research_items(
    items: List[Dict[str, Any]],
    *,
    source_key: str,
    source_label: str,
    title_field: str = "title",
    body_field: str = "body",
) -> str:
    if not items:
        return ""

    grouped = group_by_audience_and_theme(items)
    blocks: List[str] = []

    for audience in AUDIENCE_ORDER:
        themes = grouped.get(audience, {})
        if not themes:
            continue

        theme_lists: List[str] = []
        for theme in sorted(themes.keys()):
            theme_items = themes[theme]
            lis = []
            for item in theme_items[:20]:
                title = item.get(title_field) or item.get("subject") or item.get("guide_name") or "Item"
                preview = _esc((item.get(body_field) or item.get("response") or "")[:180])
                attrs = _research_item_attrs(source_key, item.get("audience", ""), item.get("theme", ""))
                lis.append(
                    f"<li {attrs}>"
                    f"<strong>{_esc(title)}</strong>"
                    f'{f"<br/><em>{preview}</em>" if preview else ""}</li>'
                )
            theme_lists.append(
                f'<section class="theme-section filterable-group" data-audience="{_esc(audience)}" '
                f'data-theme="{_esc(theme)}"><h4>{_esc(theme)} ({len(theme_items)})</h4><ul>{"".join(lis)}</ul></section>'
            )

        blocks.append(
            f'<section class="audience-section filterable-group" data-audience="{_esc(audience)}">'
            f"<h3>{_esc(audience)}</h3>"
            f'{"".join(theme_lists)}</section>'
        )

    inner = "".join(blocks)
    return (
        f'<section class="source-section" data-source="{_esc(source_key)}">'
        f"<h2>{_esc(source_label)}</h2>{inner}</section>"
    )


def _format_date(iso_date: str) -> str:
    if not iso_date:
        return ""
    return iso_date[:10]


def _render_posthog_catalog(
    items: List[Dict[str, Any]],
    synthesis: Dict[str, str],
    period_label: str = "Last 3 months",
) -> str:
    """Render full PostHog drop-off catalog grouped by funnel."""
    if not items:
        return ""

    by_funnel: Dict[str, List[Dict[str, Any]]] = {}
    for item in items:
        funnel = item.get("funnel_name", "Unknown funnel")
        by_funnel.setdefault(funnel, []).append(item)

    sections: List[str] = []
    for funnel_name in sorted(by_funnel.keys()):
        funnel_items = by_funnel[funnel_name]
        lis: List[str] = []

        for item in funnel_items:
            title = item.get("title", "Untitled")
            step = item.get("step", "")
            drop_pct = item.get("drop_percentage", 0)
            users = item.get("users_affected", 0)
            severity = item.get("severity", "MEDIUM")
            audience = item.get("audience", "")
            theme = item.get("theme", "")
            search_text = _esc(f"{title} {funnel_name} {step}".lower())
            analysis = synthesis.get(title, "")
            ai_html = (
                f'<p class="ai-snippet">{_esc(analysis)}</p>'
                if analysis and analysis != "Analysis pending."
                else ""
            )
            research_html = _render_research_list(item.get("research_context", {}))
            has_research = "No related qualitative research found." not in research_html
            research_block = (
                f'<details class="research-inline"><summary>Related research</summary>'
                f"<ul>{research_html}</ul></details>"
                if has_research
                else ""
            )
            users_display = f"{int(users):,}" if isinstance(users, (int, float)) else _esc(users)

            lis.append(
                f'<li class="filterable" data-source="posthog" '
                f'data-audience="{_esc(audience)}" data-theme="{_esc(theme)}" '
                f'data-severity="{_esc(severity)}" data-search-text="{search_text}">'
                f"{_severity_badge(severity)} "
                f"<strong>{_esc(title)}</strong>"
                f'<span class="metrics-inline"> · {drop_pct}% drop-off · {users_display} users</span>'
                f'<br/><span class="step-inline">{_esc(step)}</span>'
                f"{ai_html}"
                f"{research_block}"
                f"</li>"
            )

        sections.append(
            f'<section class="posthog-funnel-section" data-funnel="{_esc(funnel_name)}">'
            f"<h3>{_esc(funnel_name)} ({len(funnel_items)})</h3>"
            f'<ul class="posthog-list">{"".join(lis)}</ul></section>'
        )

    total = len(items)
    synthesized = len([t for t in synthesis if synthesis.get(t)])
    return (
        f'<section class="source-section" data-source="posthog">'
        f"<h2>PostHog — {period_label} ({total} drop-offs)</h2>"
        f'<p class="hint">All funnel drop-offs above threshold in the period. '
        f"Top {synthesized} include AI analysis. Use filters above or add search on this section.</p>"
        f'{"".join(sections)}</section>'
    )


def _render_dovetail_catalog(
    items: List[Dict[str, Any]],
    period_label: str = "Last 3 months",
) -> str:
    """Render full Dovetail catalog grouped by item type (insights, highlights, notes)."""
    if not items:
        return ""

    by_type: Dict[str, List[Dict[str, Any]]] = {
        "insight": [],
        "highlight": [],
        "note": [],
    }
    for item in items:
        item_type = item.get("type", "note")
        by_type.setdefault(item_type, []).append(item)

    type_labels = {
        "insight": "Insights",
        "highlight": "Highlights",
        "note": "Notes",
    }

    sections: List[str] = []
    for item_type in ("insight", "highlight", "note"):
        type_items = by_type.get(item_type, [])
        if not type_items:
            continue

        lis: List[str] = []
        for item in type_items:
            title = item.get("title") or "Untitled"
            body = item.get("body") or item.get("preview") or ""
            url = item.get("url", "")
            date = _format_date(item.get("created_at", ""))
            search_text = _esc(f"{title} {body}".lower())
            attrs = _research_item_attrs("dovetail", item.get("audience", ""), item.get("theme", ""))
            title_html = (
                f'<a href="{_esc(url)}">{_esc(title)}</a>' if url else _esc(title)
            )
            preview_html = f'<br/><em>{_esc(body[:240])}</em>' if body else ""
            date_html = f' <span class="date">{_esc(date)}</span>' if date else ""
            lis.append(
                f'<li {attrs} data-type="{_esc(item_type)}" data-search-text="{search_text}">'
                f'<span class="pill type">{_esc(type_labels.get(item_type, item_type))}</span> '
                f"{title_html}{date_html}"
                f"{preview_html}</li>"
            )

        sections.append(
            f'<section class="dovetail-type-section" data-dovetail-type="{_esc(item_type)}">'
            f"<h3>{type_labels[item_type]} ({len(type_items)})</h3>"
            f'<ul class="dovetail-list">{"".join(lis)}</ul></section>'
        )

    total = len(items)
    return (
        f'<section class="source-section" data-source="dovetail">'
        f"<h2>Dovetail — {period_label} ({total} items)</h2>"
        f'<p class="hint">Full catalog for the period. Use filters above or add search on this section.</p>'
        f'{"".join(sections)}</section>'
    )


def _render_unmatched_research(
    freshdesk_tickets: List[Dict[str, Any]],
    pendo_feedback: List[Dict[str, Any]],
    dovetail_insights: List[Dict[str, Any]],
    outset_studies: List[Dict[str, Any]],
    period_label: str = "Last 3 months",
) -> str:
    sections = []

    freshdesk_html = _render_grouped_research_items(
        freshdesk_tickets,
        source_key="freshdesk",
        source_label=f"Freshdesk support signals ({period_label})",
        title_field="subject",
        body_field="body",
    )
    if freshdesk_html:
        sections.append(freshdesk_html)

    pendo_html = _render_grouped_research_items(
        pendo_feedback,
        source_key="pendo",
        source_label=f"Pendo feedback ({period_label})",
        title_field="guide_name",
        body_field="response",
    )
    if pendo_html:
        sections.append(pendo_html)

    dovetail_html = _render_dovetail_catalog(dovetail_insights, period_label=period_label)
    if dovetail_html:
        sections.append(dovetail_html)

    outset_html = _render_grouped_research_items(
        outset_studies,
        source_key="outset",
        source_label=f"Outset studies ({period_label})",
        title_field="title",
        body_field="summary",
    )
    if outset_html:
        sections.append(outset_html)

    return "\n".join(sections)


def _collect_themes(payload: Dict[str, Any]) -> List[str]:
    themes: set[str] = set()
    for key in (
        "issues",
        "posthog_dropoffs",
        "pendo_feedback",
        "pendo_analytics",
        "dovetail_insights",
        "freshdesk_tickets",
        "outset_studies",
    ):
        for item in payload.get(key, []):
            if item.get("theme"):
                themes.add(str(item["theme"]))
    return sorted(themes)


def _collect_product_areas(items: List[Dict[str, Any]]) -> List[str]:
    areas = {str(item.get("product_area") or "").strip() for item in items}
    return sorted(a for a in areas if a)


def _truncate(text: str, limit: int = 120) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def _humanize_step(step: str) -> str:
    """Turn 'event_a → event_b' into a short readable transition."""
    raw = (step or "").strip()
    if "→" in raw:
        parts = [p.strip() for p in raw.split("→", 1)]
        if len(parts) == 2:
            left = parts[0].split(":")[-1].replace("_", " ").strip()
            right = parts[1].split(":")[-1].replace("_", " ").strip()
            return f"{left} → {right}"
    return raw.replace("_", " ")


def _resolve_product_area(item: Dict[str, Any]) -> str:
    if item.get("product_area"):
        return str(item["product_area"])
    return classify_product_area(item)


def _ai_first_line(analysis: str) -> str:
    if not analysis or analysis == "Analysis pending.":
        return ""
    line = analysis.strip().split("\n", 1)[0].strip()
    # Skip placeholder synthesis that restates the metric
    if line.lower().startswith("drop-off detected"):
        return ""
    return _truncate(line, 140)


def _source_badge(source: str) -> str:
    colors = {
        "posthog": "#e3f2fd",
        "dovetail": "#ede7f6",
        "outset": "#e8f5e9",
        "pendo": "#fff3e0",
        "freshdesk": "#fce4ec",
    }
    bg = colors.get(source, "#f5f5f5")
    return (
        f'<span class="badge badge-source" style="background:{bg}">'
        f"{_esc(SOURCE_LABELS.get(source, source))}</span>"
    )


def _status_badge(status: str, severity: str = "") -> str:
    label = severity or status or "—"
    colors = {
        "HIGH": "#d32f2f",
        "MEDIUM": "#f57c00",
        "Insight": "#5e35b1",
        "Highlight": "#3949ab",
        "Note": "#546e7a",
        "Study": "#2e7d32",
        "Friction": "#c62828",
        "Page": "#00838f",
        "Feature": "#6a1b9a",
        "Feedback": "#ef6c00",
        "Bug": "#b42318",
        "Ticket": "#c2185b",
    }
    color = colors.get(label, "#757575")
    if label in ("HIGH", "MEDIUM"):
        return f'<span class="badge badge-status" style="background:{color}">{_esc(label)}</span>'
    return f'<span class="badge badge-type" style="background:{color}">{_esc(label)}</span>'


def _item_date_sort_key(iso_date: str) -> str:
    """Normalize ISO timestamps for descending sort (empty dates sort last)."""
    return (iso_date or "").strip()


def _clean_pendo_name(name: str) -> str:
    """Drop 'Brand - Discover:' / 'Partner - Home:' prefixes already shown in product area."""
    raw = (name or "").strip()
    if ": " in raw and raw.lower().startswith(("brand -", "partner -", "(don't use)")):
        return raw.split(": ", 1)[1].strip() or raw
    return raw


def _collect_listing_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Flatten all sources into unified table rows, newest first."""
    items: List[Dict[str, Any]] = []
    synthesis = payload.get("synthesis", {})
    period_end = (payload.get("period") or {}).get("end", "")
    generated_at = payload.get("generated_at", "")
    # PostHog funnel stats cover the period; use period end as the report date
    posthog_date = period_end or _format_date(generated_at) or ""
    idx = 0

    def add(**kwargs: Any) -> None:
        nonlocal idx
        kwargs.setdefault("id", f"row-{idx}")
        raw_date = str(kwargs.pop("date", "") or "")
        kwargs["date"] = raw_date
        kwargs["date_display"] = _format_date(raw_date) or "—"
        product_area = kwargs.get("product_area") or "Cross-platform"
        kwargs["product_area"] = product_area
        signal = kwargs.get("signal") or classify_listing_signal(
            source=str(kwargs.get("source") or ""),
            status=str(kwargs.get("status") or ""),
            title=str(kwargs.get("title") or ""),
            body=str(kwargs.get("subtitle") or ""),
            item_type=str(kwargs.get("status") or ""),
        )
        kwargs["signal"] = signal
        kwargs["signal_label"] = SIGNAL_LABELS.get(signal, signal)
        search = kwargs.get("search_text", "")
        kwargs["search_text"] = f"{search} {product_area} {signal} {kwargs['signal_label']}".lower().strip()
        idx += 1
        items.append(kwargs)

    for issue in payload.get("posthog_dropoffs", payload.get("issues", [])):
        funnel = issue.get("funnel_name") or "Funnel"
        drop = issue.get("drop_percentage", 0)
        step = issue.get("step", "")
        users = issue.get("users_affected", 0)
        users_display = f"{int(users):,}" if isinstance(users, (int, float)) else str(users)
        raw_title = issue.get("title", "Untitled")
        analysis = synthesis.get(raw_title, "")
        human_step = _humanize_step(step)
        ai_line = _ai_first_line(analysis)
        subtitle = ai_line or f"{human_step} · {users_display} users affected"
        product_area = _resolve_product_area(issue)
        title = f"{funnel}: {drop}% drop"
        add(
            id=f"posthog-{idx}",
            source="posthog",
            title=title,
            subtitle=subtitle,
            audience=issue.get("audience", ""),
            theme=issue.get("theme", ""),
            product_area=product_area,
            severity=issue.get("severity", ""),
            status=issue.get("severity", ""),
            signal="quant",
            metric=f"{drop}% drop · {users_display} users",
            date=issue.get("created_at") or posthog_date,
            search_text=f"{title} {funnel} {step} {human_step} {ai_line}",
            detail_kind="posthog",
            detail_data={"issue": issue, "analysis": analysis},
        )

    type_labels = {"insight": "Insight", "highlight": "Highlight", "note": "Note"}
    for item in payload.get("dovetail_insights", []):
        raw_title = item.get("title") or "Untitled"
        body = item.get("body") or item.get("preview") or ""
        item_type = type_labels.get(item.get("type", ""), item.get("type", "Note") or "Note")
        project = item.get("project_title") or ""
        product_area = _resolve_product_area(item)
        is_voice, kind = is_dovetail_user_voice(item)
        signal = classify_listing_signal(
            source="dovetail",
            status=item_type,
            title=raw_title,
            body=body,
            item_type=item.get("type") or item_type,
            item=item,
        )
        if kind == "quote":
            title = f"User quote: {_truncate(body or raw_title, 90)}"
            subtitle = f"Dovetail {item_type} · {_truncate(raw_title, 80)}" if body else f"Dovetail {item_type}"
        elif kind == "bug":
            title = f"Bug note: {raw_title}"
            subtitle = _truncate(body) or "Dovetail bug / issue"
        elif kind == "feedback_note":
            title = f"Research feedback: {raw_title}"
            subtitle = _truncate(body) or "Dovetail feedback / NPS"
        else:
            title = f"{item_type}: {raw_title}"
            subtitle = " · ".join(p for p in (_truncate(body), project) if p)
        add(
            source="dovetail",
            title=title,
            subtitle=subtitle,
            audience=item.get("audience", ""),
            theme=item.get("theme", ""),
            product_area=product_area,
            severity="HIGH" if signal == "bug" else "",
            status="Bug" if signal == "bug" else ("Feedback" if is_voice else item_type),
            signal=signal,
            metric=project or "—",
            date=item.get("created_at", ""),
            search_text=f"{title} {raw_title} {body} {project}",
            detail_kind="dovetail",
            detail_data={"item": item},
        )

    for item in payload.get("outset_studies", []):
        raw_title = item.get("title") or "Untitled study"
        summary = item.get("summary") or item.get("body") or ""
        method = item.get("interview_method") or ""
        product_area = _resolve_product_area(item)
        is_voice = is_outset_user_voice(item)
        signal = classify_listing_signal(
            source="outset",
            status="Study",
            title=raw_title,
            body=summary,
            item_type="Study",
            item=item,
        )
        title = f"Study feedback: {raw_title}" if is_voice else f"Study: {raw_title}"
        subtitle_bits = [p for p in (method, _truncate(summary)) if p]
        add(
            source="outset",
            title=title,
            subtitle=" · ".join(subtitle_bits) or "Outset study",
            audience=item.get("audience", ""),
            theme=item.get("theme", ""),
            product_area=product_area,
            severity="",
            status="Feedback" if is_voice else "Study",
            signal=signal,
            metric=method or "—",
            date=item.get("created_at", ""),
            search_text=f"{raw_title} {summary} {method}",
            detail_kind="outset",
            detail_data={"item": item},
        )

    for item in payload.get("pendo_analytics", []):
        name = item.get("title") or "Pendo entity"
        display_name = _clean_pendo_name(name)
        item_type = item.get("type") or "Page"
        product_area = _resolve_product_area(item)
        visitors = item.get("visitors")
        events = item.get("events")
        rage = item.get("rage_clicks") or 0
        dead = item.get("dead_clicks") or 0
        if item_type == "Friction":
            title = f"{product_area}: friction on {display_name}"
            subtitle = f"{int(rage):,} rage · {int(dead):,} dead clicks"
            if isinstance(visitors, (int, float)):
                subtitle += f" · {int(visitors):,} visitors"
        else:
            verb = "high usage" if (events or 0) > 0 else "usage"
            title = f"{product_area}: {verb} — {display_name}"
            parts = []
            if isinstance(events, (int, float)):
                parts.append(f"{int(events):,} events")
            if isinstance(visitors, (int, float)):
                parts.append(f"{int(visitors):,} visitors")
            subtitle = " · ".join(parts) or (item.get("subtitle") or item.get("body") or "")
        add(
            source="pendo",
            title=title,
            subtitle=subtitle,
            audience=item.get("audience", ""),
            theme=item.get("theme", ""),
            product_area=product_area,
            severity="HIGH" if item_type == "Friction" else "",
            status=item_type,
            signal="friction" if item_type == "Friction" else "quant",
            metric=item.get("metric") or "—",
            date=str(item.get("created_at") or item.get("timestamp") or ""),
            search_text=f"{title} {name} {subtitle}",
            detail_kind="pendo_analytics",
            detail_data={"item": item},
        )

    for item in payload.get("pendo_feedback", []):
        meta = classify_feedback_item(item)
        product_area = _resolve_product_area({
            **item,
            "title": meta["display_title"],
            "body": meta.get("comment") or item.get("response") or "",
        })
        add(
            source="pendo",
            title=meta["display_title"],
            subtitle=meta["display_subtitle"],
            audience=item.get("audience", ""),
            theme=item.get("theme", "") or (" · ".join(meta["themes"][:2]) if meta["themes"] else ""),
            product_area=product_area,
            severity="HIGH" if meta["signal"] == "bug" else "",
            status="Bug" if meta["signal"] == "bug" else "Feedback",
            signal=meta["signal"],
            metric=" · ".join(meta["themes"][:3]) if meta["themes"] else (item.get("poll_type") or "NPS"),
            date=str(item.get("timestamp") or item.get("created_at") or ""),
            search_text=f"{meta['display_title']} {meta.get('comment','')} {' '.join(meta['themes'])}",
            detail_kind="pendo",
            detail_data={"item": item, "parsed": meta},
        )

    for item in payload.get("freshdesk_tickets", []):
        raw_title = item.get("subject") or "Support ticket"
        body = item.get("body") or ""
        product_area = _resolve_product_area(item)
        add(
            source="freshdesk",
            title=f"Support: {raw_title}",
            subtitle=_truncate(body),
            audience=item.get("audience", ""),
            theme=item.get("theme", ""),
            product_area=product_area,
            severity="",
            status=item.get("status") or item.get("ticket_type") or "Ticket",
            signal="support",
            metric="—",
            date=str(item.get("created_at") or ""),
            search_text=f"{raw_title} {body}",
            detail_kind="freshdesk",
            detail_data={"item": item},
        )

    items.sort(key=lambda row: _item_date_sort_key(row.get("date", "")), reverse=True)
    return items


def _render_slideout_detail(item: Dict[str, Any]) -> str:
    kind = item.get("detail_kind")
    data = item.get("detail_data", {})

    if kind == "posthog":
        issue = data.get("issue", {})
        analysis = data.get("analysis", "")
        context = issue.get("research_context", {})
        metrics = issue.get("metrics", {})
        analysis_block = ""
        if analysis and analysis != "Analysis pending.":
            analysis_block = (
                f'<section class="detail-block ai-block">'
                f"<h3>AI analysis</h3><p>{_esc(analysis)}</p></section>"
            )
        users = issue.get("users_affected", 0)
        users_str = f"{int(users):,}" if isinstance(users, (int, float)) else str(users)
        return (
            f'<section class="detail-block">'
            f"<h3>Funnel metrics</h3>"
            f"<dl>"
            f"<dt>Funnel</dt><dd>{_esc(issue.get('funnel_name', ''))}</dd>"
            f"<dt>Step transition</dt><dd>{_esc(issue.get('step', ''))}</dd>"
            f"<dt>Drop-off</dt><dd>{issue.get('drop_percentage', 0)}%</dd>"
            f"<dt>Users at step</dt><dd>{users_str}</dd>"
            f"<dt>From count</dt><dd>{metrics.get('step_from', '—')}</dd>"
            f"<dt>To count</dt><dd>{metrics.get('step_to', '—')}</dd>"
            f"</dl></section>"
            f"{analysis_block}"
            f'<section class="detail-block"><h3>Related research</h3>'
            f"<ul>{_render_research_list(context)}</ul></section>"
            f'<p class="detail-links"><a href="{_esc(issue.get("posthog_link", "#"))}" '
            f'target="_blank" rel="noopener">Open in PostHog</a></p>'
        )

    if kind == "dovetail":
        d = data.get("item", {})
        body = d.get("body") or d.get("preview") or ""
        link = d.get("url", "")
        link_html = (
            f'<p class="detail-links"><a href="{_esc(link)}" target="_blank" rel="noopener">'
            f"Open in Dovetail</a></p>"
            if link
            else ""
        )
        return (
            f'<section class="detail-block"><h3>Preview</h3><p>{_esc(body) or "—"}</p></section>'
            f"<dl>"
            f"<dt>Type</dt><dd>{_esc(d.get('type', ''))}</dd>"
            f"<dt>Project</dt><dd>{_esc(d.get('project_title') or '—')}</dd>"
            f"<dt>Created</dt><dd>{_esc(_format_date(d.get('created_at', '')))}</dd>"
            f"</dl>"
            f"{link_html}"
        )

    if kind == "outset":
        d = data.get("item", {})
        summary = d.get("summary") or d.get("body") or ""
        link = d.get("url", "")
        link_html = (
            f'<p class="detail-links"><a href="{_esc(link)}" target="_blank" rel="noopener">'
            f"Open study</a></p>"
            if link
            else ""
        )
        return (
            f'<section class="detail-block"><h3>Summary</h3><p>{_esc(summary) or "—"}</p></section>'
            f"<dl>"
            f"<dt>Method</dt><dd>{_esc(d.get('interview_method') or '—')}</dd>"
            f"<dt>Language</dt><dd>{_esc(d.get('language_code') or '—')}</dd>"
            f"<dt>Active</dt><dd>{_esc(d.get('active', '—'))}</dd>"
            f"</dl>"
            f"{link_html}"
        )

    if kind == "pendo":
        d = data.get("item", {})
        parsed = data.get("parsed") or classify_feedback_item(d)
        comment = parsed.get("comment") or d.get("response", "")
        themes = parsed.get("themes") or []
        return (
            f'<section class="detail-block"><h3>What the user wrote</h3>'
            f"<p>{_esc(comment) if comment else 'No written comment — theme tags only.'}</p></section>"
            f"<dl>"
            f"<dt>Signal</dt><dd>{_esc(SIGNAL_LABELS.get(parsed.get('signal', ''), parsed.get('signal', '')))}</dd>"
            f"<dt>NPS themes</dt><dd>{_esc(', '.join(themes) if themes else '—')}</dd>"
            f"<dt>Guide</dt><dd>{_esc(d.get('guide_name') or d.get('title', ''))}</dd>"
            f"<dt>Poll type</dt><dd>{_esc(d.get('poll_type') or '—')}</dd>"
            f"<dt>Follow-up</dt><dd>{_esc(parsed.get('followup') or '—')}</dd>"
            f"<dt>Visitor</dt><dd>{_esc(d.get('visitor_id') or '—')}</dd>"
            f"<dt>Date</dt><dd>{_esc(_format_date(str(d.get('created_at') or d.get('timestamp') or '')))}</dd>"
            f"</dl>"
        )

    if kind == "pendo_analytics":
        d = data.get("item", {})
        return (
            f'<section class="detail-block"><h3>Product analytics</h3>'
            f"<p>{_esc(d.get('subtitle') or d.get('body') or '')}</p></section>"
            f"<dl>"
            f"<dt>Type</dt><dd>{_esc(d.get('type') or '—')}</dd>"
            f"<dt>Events</dt><dd>{int(d.get('events') or 0):,}</dd>"
            f"<dt>Visitors</dt><dd>{int(d.get('visitors') or 0):,}</dd>"
            f"<dt>Rage clicks</dt><dd>{int(d.get('rage_clicks') or 0):,}</dd>"
            f"<dt>Dead clicks</dt><dd>{int(d.get('dead_clicks') or 0):,}</dd>"
            f"<dt>Entity ID</dt><dd>{_esc(d.get('entity_id') or '—')}</dd>"
            f"</dl>"
        )

    if kind == "freshdesk":
        d = data.get("item", {})
        link = d.get("url", "")
        link_html = (
            f'<p class="detail-links"><a href="{_esc(link)}" target="_blank" rel="noopener">'
            f"Open ticket</a></p>"
            if link
            else ""
        )
        return (
            f'<section class="detail-block"><h3>Ticket body</h3>'
            f"<p>{_esc(d.get('body', ''))}</p></section>"
            f"<dl>"
            f"<dt>Status</dt><dd>{_esc(d.get('status') or '—')}</dd>"
            f"<dt>Type</dt><dd>{_esc(d.get('ticket_type') or '—')}</dd>"
            f"</dl>"
            f"{link_html}"
        )

    return "<p>No details available.</p>"


def _render_listing_table(items: List[Dict[str, Any]]) -> str:
    if not items:
        return '<p class="empty">No findings in this period.</p>'

    rows: List[str] = []
    templates: List[str] = []

    for item in items:
        row_id = item["id"]
        audience = item.get("audience") or "—"
        product_area = item.get("product_area") or "—"
        theme = item.get("theme") or "—"
        templates.append(
            f'<template id="detail-{row_id}">'
            f'<dl class="detail-meta">'
            f"<dt>Product area</dt><dd>{_esc(product_area)}</dd>"
            f"<dt>Theme</dt><dd>{_esc(theme)}</dd>"
            f"<dt>Audience</dt><dd>{_esc(audience)}</dd>"
            f"</dl>"
            f"{_render_slideout_detail(item)}"
            f"</template>"
        )
        date_display = item.get("date_display") or "—"
        rows.append(
            f'<tr class="listing-row filterable" tabindex="0" role="button" '
            f'data-row-id="{row_id}" '
            f'data-source="{_esc(item["source"])}" '
            f'data-audience="{_esc(item.get("audience", ""))}" '
            f'data-theme="{_esc(item.get("theme", ""))}" '
            f'data-product-area="{_esc(item.get("product_area", ""))}" '
            f'data-signal="{_esc(item.get("signal", ""))}" '
            f'data-severity="{_esc(item.get("severity", ""))}" '
            f'data-date="{_esc(item.get("date", ""))}" '
            f'data-search-text="{_esc(item.get("search_text", ""))}">'
            f'<td class="cell-date">{_esc(date_display)}</td>'
            f"<td>{_source_badge(item['source'])}</td>"
            f'<td class="cell-finding">'
            f'<div class="finding-title">{_esc(item["title"])}</div>'
            f'<div class="finding-sub">{_esc(item.get("subtitle", ""))}</div>'
            f"</td>"
            f'<td><span class="pill product-area">{_esc(product_area)}</span></td>'
            f'<td><span class="pill audience">{_esc(audience)}</span></td>'
            f'<td><span class="pill signal signal-{_esc(item.get("signal", ""))}">'
            f'{_esc(item.get("signal_label") or item.get("signal") or "—")}</span></td>'
            f"<td>{_status_badge(item.get('status', ''), item.get('severity', ''))}</td>"
            f'<td class="cell-metric">{_esc(item.get("metric", ""))}</td>'
            f"</tr>"
        )

    return (
        f'{"".join(templates)}'
        f'<div class="table-wrap">'
        f'<table class="listing-table" aria-label="Research findings">'
        f"<thead><tr>"
        f'<th class="cell-date">Date <span class="sort-hint" title="Newest first">↓</span></th>'
        f"<th>Source</th><th>Finding</th><th>Product area</th><th>Audience</th>"
        f"<th>Signal</th><th>Status</th><th>Metric</th>"
        f"</tr></thead>"
        f'<tbody id="listing-body">{"".join(rows)}</tbody>'
        f"</table></div>"
    )


def _render_filter_bar(payload: Dict[str, Any], listing_items: Optional[List[Dict[str, Any]]] = None) -> str:
    theme_options = "".join(
        f'<option value="{_esc(theme)}">{_esc(theme)}</option>'
        for theme in _collect_themes(payload)
    )
    area_options = "".join(
        f'<option value="{_esc(area)}">{_esc(area)}</option>'
        for area in _collect_product_areas(listing_items or [])
    )
    counts = payload.get("source_counts", {})
    source_options = "".join(
        f'<option value="{source}">{SOURCE_LABELS[source]} ({counts.get(source, 0)})</option>'
        for source in SOURCE_ORDER
        if counts.get(source, 0) > 0 or source == "posthog"
    )
    return f"""
    <section class="filters" aria-label="Filter findings">
      <div class="filter-row">
        <label>
          Source
          <select id="filter-source">
            <option value="all">All sources ({sum(counts.values())})</option>
            {source_options}
          </select>
        </label>
        <label>
          Audience
          <select id="filter-audience">
            <option value="all">All audiences</option>
            <option value="Brand">Brand</option>
            <option value="Partner">Partner</option>
            <option value="Shared">Shared</option>
          </select>
        </label>
        <label>
          Product area
          <select id="filter-product-area">
            <option value="all">All product areas</option>
            {area_options}
          </select>
        </label>
        <label>
          Theme
          <select id="filter-theme">
            <option value="all">All themes</option>
            {theme_options}
          </select>
        </label>
        <label>
          Signal
          <select id="filter-signal">
            <option value="all">All signals</option>
            <option value="user_reports">User reports (feedback + bugs + friction + support)</option>
            <option value="user_feedback">User feedback</option>
            <option value="bug">Bug reports</option>
            <option value="friction">Friction</option>
            <option value="support">Support</option>
            <option value="quant">Quant drop-offs</option>
            <option value="research">Research</option>
          </select>
        </label>
        <label>
          Severity
          <select id="filter-severity">
            <option value="all">All severities</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
          </select>
        </label>
        <label class="search-label">
          Search
          <input type="search" id="filter-search" placeholder="Filter by keyword…" />
        </label>
        <button type="button" id="filter-reset" class="filter-reset">Reset</button>
      </div>
      <div class="source-counts">
        {''.join(
            f'<span class="pill source-pill" data-source="{source}">'
            f'{SOURCE_LABELS[source]}: <strong>{counts.get(source, 0)}</strong></span>'
            for source in SOURCE_ORDER
        )}
      </div>
      <p class="filter-status" id="filter-status"></p>
    </section>
    """


def _render_app_script() -> str:
    return """
  <script>
    (function () {
      const audienceEl = document.getElementById("filter-audience");
      const themeEl = document.getElementById("filter-theme");
      const areaEl = document.getElementById("filter-product-area");
      const severityEl = document.getElementById("filter-severity");
      const signalEl = document.getElementById("filter-signal");
      const sourceEl = document.getElementById("filter-source");
      const searchEl = document.getElementById("filter-search");
      const resetEl = document.getElementById("filter-reset");
      const statusEl = document.getElementById("filter-status");
      const backdrop = document.getElementById("slideout-backdrop");
      const slideout = document.getElementById("slideout");
      const slideoutTitle = document.getElementById("slideout-title");
      const slideoutMeta = document.getElementById("slideout-meta");
      const slideoutBody = document.getElementById("slideout-body");
      const slideoutClose = document.getElementById("slideout-close");

      function matchesFilters(el) {
        const q = (searchEl.value || "").trim().toLowerCase();
        const audience = audienceEl.value;
        const theme = themeEl.value;
        const area = areaEl.value;
        const severity = severityEl.value;
        const signal = signalEl ? signalEl.value : "all";
        const source = sourceEl.value;
        const itemAudience = el.dataset.audience || "";
        const itemTheme = el.dataset.theme || "";
        const itemArea = el.dataset.productArea || "";
        const itemSeverity = el.dataset.severity || "";
        const itemSignal = el.dataset.signal || "";
        const itemSource = el.dataset.source || "";
        const searchText = el.dataset.searchText || "";

        if (source !== "all" && itemSource !== source) return false;
        if (audience !== "all" && itemAudience !== audience) return false;
        if (area !== "all" && itemArea !== area) return false;
        if (theme !== "all" && itemTheme !== theme) return false;
        if (severity !== "all" && itemSeverity && itemSeverity !== severity) return false;
        if (signal === "user_reports") {
          if (!["user_feedback", "bug", "friction", "support"].includes(itemSignal)) return false;
        } else if (signal !== "all" && itemSignal !== signal) {
          return false;
        }
        if (q && !searchText.includes(q)) return false;
        return true;
      }

      function applyFilters() {
        const rows = document.querySelectorAll(".listing-row.filterable");
        let visibleCount = 0;

        rows.forEach((el) => {
          const show = matchesFilters(el);
          el.classList.toggle("is-filtered-out", !show);
          if (show) visibleCount += 1;
        });

        const parts = [];
        if (sourceEl.value !== "all") parts.push(sourceEl.value);
        if (audienceEl.value !== "all") parts.push(audienceEl.value);
        if (areaEl.value !== "all") parts.push(areaEl.value);
        if (themeEl.value !== "all") parts.push(themeEl.value);
        if (signalEl && signalEl.value !== "all") parts.push(signalEl.options[signalEl.selectedIndex].text);
        if (severityEl.value !== "all") parts.push(severityEl.value + " severity");
        if (searchEl.value.trim()) parts.push('"' + searchEl.value.trim() + '"');
        statusEl.textContent = parts.length
          ? `Showing ${visibleCount} of ${rows.length} · ${parts.join(" · ")}`
          : `Showing all ${visibleCount} items`;
      }

      function openSlideout(row) {
        const rowId = row.dataset.rowId;
        const tmpl = document.getElementById("detail-" + rowId);
        if (!tmpl) return;

        const titleEl = row.querySelector(".finding-title");
        const subEl = row.querySelector(".finding-sub");
        slideoutTitle.textContent = titleEl ? titleEl.textContent : "Details";
        slideoutMeta.textContent = subEl ? subEl.textContent : "";
        slideoutBody.innerHTML = tmpl.innerHTML;

        backdrop.classList.remove("hidden");
        slideout.classList.add("open");
        document.body.classList.add("slideout-open");
        slideoutClose.focus();
      }

      function closeSlideout() {
        backdrop.classList.add("hidden");
        slideout.classList.remove("open");
        document.body.classList.remove("slideout-open");
        slideoutBody.innerHTML = "";
      }

      document.getElementById("listing-body").addEventListener("click", (e) => {
        const row = e.target.closest(".listing-row");
        if (row && !row.classList.contains("is-filtered-out")) openSlideout(row);
      });

      document.getElementById("listing-body").addEventListener("keydown", (e) => {
        if (e.key !== "Enter" && e.key !== " ") return;
        const row = e.target.closest(".listing-row");
        if (row) {
          e.preventDefault();
          openSlideout(row);
        }
      });

      slideoutClose.addEventListener("click", closeSlideout);
      backdrop.addEventListener("click", closeSlideout);

      [sourceEl, audienceEl, areaEl, themeEl, severityEl, signalEl].filter(Boolean).forEach((el) => {
        el.addEventListener("change", applyFilters);
      });
      searchEl.addEventListener("input", applyFilters);
      resetEl.addEventListener("click", () => {
        sourceEl.value = "all";
        audienceEl.value = "all";
        areaEl.value = "all";
        themeEl.value = "all";
        severityEl.value = "all";
        if (signalEl) signalEl.value = "all";
        searchEl.value = "";
        applyFilters();
      });

      applyFilters();

      // --- Ask AI bridge (copy prompt → Cursor / Claude / etc.) ---
      const askFab = document.getElementById("ask-fab");
      const askPanel = document.getElementById("ask-panel");
      const askBackdrop = document.getElementById("ask-backdrop");
      const askClose = document.getElementById("ask-close");
      const askQuestion = document.getElementById("ask-question");
      const askPreview = document.getElementById("ask-preview");
      const askCopy = document.getElementById("ask-copy");
      const askStatus = document.getElementById("ask-status");
      const askAudienceEls = () => document.querySelectorAll('input[name="ask-audience"]');

      function selectedAskAudience() {
        const checked = document.querySelector('input[name="ask-audience"]:checked');
        return (checked && checked.value) || "both";
      }

      function audienceScopeLine(scope) {
        if (scope === "brand") {
          return "Audience scope: Brand only (exclude Partner-only findings; Shared OK when it affects Brand).";
        }
        if (scope === "partner") {
          return "Audience scope: Partner only (exclude Brand-only findings; Shared OK when it affects Partner).";
        }
        return "Audience scope: Brand and Partner (compare both; call out Shared carefully).";
      }

      function syncAskAudienceFromFilters() {
        const filterAud = audienceEl.value;
        let scope = "both";
        if (filterAud === "Brand") scope = "brand";
        else if (filterAud === "Partner") scope = "partner";
        const el = document.querySelector('input[name="ask-audience"][value="' + scope + '"]');
        if (el) el.checked = true;
      }

      function currentFilterSummary() {
        const parts = [];
        if (sourceEl.value !== "all") parts.push("Source: " + sourceEl.value);
        if (audienceEl.value !== "all") parts.push("Audience filter: " + audienceEl.value);
        if (areaEl.value !== "all") parts.push("Product area: " + areaEl.value);
        if (themeEl.value !== "all") parts.push("Theme: " + themeEl.value);
        if (severityEl.value !== "all") parts.push("Severity: " + severityEl.value);
        if (searchEl.value.trim()) parts.push('Search: "' + searchEl.value.trim() + '"');
        return parts.length ? parts.join(" · ") : "None (full pack)";
      }

      function buildAskPrompt() {
        const scope = selectedAskAudience();
        const question = (askQuestion.value || "").trim() || (
          scope === "brand"
            ? "What are the highest-priority Brand UX issues this period, and which findings should I dig into first?"
            : scope === "partner"
              ? "What are the highest-priority Partner UX issues this period, and which findings should I dig into first?"
              : "What are the highest-priority Brand and Partner UX issues this period, and where do they diverge or overlap?"
        );
        const reportUrl = askFab.dataset.reportUrl || window.location.href;
        const jsonUrl = askFab.dataset.jsonUrl || "";
        const jsonPath = askFab.dataset.jsonPath || "research-agent/docs/research/latest.json";
        const period = askFab.dataset.periodLabel || "";
        const week = askFab.dataset.weekStart || "";
        const dataLine = jsonUrl
          ? "Report pack (fetch this JSON): " + jsonUrl
          : "Report pack: " + jsonPath + " (or open the HTML report URL below)";

        return [
          "Answer a UX research question using the latest connected MCP data plus the Research Insight Monitor pack.",
          "",
          audienceScopeLine(scope),
          dataLine,
          "HTML report: " + (reportUrl || window.location.href),
          period ? "Period: " + period + (week ? " · week of " + week : "") : null,
          "Active filters from the report UI: " + currentFilterSummary(),
          "",
          "Required MCPs (tell me which are connected vs missing before answering deeply):",
          "- PostHog MCP — funnels, drop-offs, trends, session replay (Impact Membersite)",
          "- Pendo MCP — pages/features, friction, guides, poll/NPS feedback",
          "Optional MCPs / sources (use if connected; say if not):",
          "- Dovetail — qualitative insights / highlights / notes",
          "- Outset — study summaries",
          "- Freshdesk / BigQuery — support tickets (often via research pack if MCP unavailable)",
          "",
          "How to get data:",
          "1. Check which of the MCPs above are available in this harness and list Connected vs Not connected.",
          "2. Use connected MCPs to pull the latest data for the audience scope (do not rely only on stale memory).",
          "3. Also fetch/read the report pack JSON for this period’s Verified findings; reconcile pack vs live when they differ.",
          "4. Prefer the master skill design-thinking-ux (Design Thinking UX) for a guided Empathize → Test run. It asks intake questions and invokes phase skills. For a single Empathize step, use research-synthesis, data-analyze, synthesize-research, or user-research.",
          "",
          "Rules:",
          "- Lead with Verified evidence; cite source + title/date (and link when present).",
          "- Do not invent metrics. If an MCP is missing, say what you could not query.",
          "- Respect the audience scope above. Separate Brand vs Partner; call out Shared carefully.",
          "- End with 2–4 concrete next questions or deep-dives I can ask.",
          "",
          "My question:",
          question,
        ].filter((line) => line !== null).join("\\n");
      }

      function refreshAskPreview() {
        if (askPreview) askPreview.value = buildAskPrompt();
      }

      function openAsk() {
        closeSlideout();
        syncAskAudienceFromFilters();
        refreshAskPreview();
        askBackdrop.classList.remove("hidden");
        askPanel.classList.add("open");
        askPanel.setAttribute("aria-hidden", "false");
        askQuestion.focus();
      }

      function closeAsk() {
        askBackdrop.classList.add("hidden");
        askPanel.classList.remove("open");
        askPanel.setAttribute("aria-hidden", "true");
        askStatus.textContent = "";
      }

      askFab.addEventListener("click", openAsk);
      askClose.addEventListener("click", closeAsk);
      askBackdrop.addEventListener("click", closeAsk);
      askQuestion.addEventListener("input", refreshAskPreview);
      askAudienceEls().forEach((el) => el.addEventListener("change", refreshAskPreview));
      [sourceEl, audienceEl, areaEl, themeEl, severityEl].forEach((el) => {
        el.addEventListener("change", () => {
          if (askPanel.classList.contains("open")) refreshAskPreview();
        });
      });
      searchEl.addEventListener("input", () => {
        if (askPanel.classList.contains("open")) refreshAskPreview();
      });

      askCopy.addEventListener("click", async () => {
        const text = buildAskPrompt();
        askPreview.value = text;
        try {
          await navigator.clipboard.writeText(text);
          askStatus.textContent = "Copied — paste into Cursor, Claude, ChatGPT, or your harness.";
        } catch (err) {
          askPreview.select();
          askStatus.textContent = "Select the prompt and copy manually (Cmd/Ctrl+C).";
        }
      });

      document.addEventListener("keydown", (e) => {
        if (e.key !== "Escape") return;
        if (askPanel.classList.contains("open")) closeAsk();
        else closeSlideout();
      });
    })();
  </script>
"""


def render_html_report(payload: Dict[str, Any], *, at_root: bool = False) -> str:
    summary = payload["summary"]
    week = payload["week_start"]
    period = payload.get("period", {})
    period_label = period.get("label", "Last 3 months")
    period_start = period.get("start", "")
    period_end = period.get("end", "")
    counts = payload.get("source_counts", {})
    total_items = sum(counts.values())
    synthesized = summary.get("ai_synthesized_count", len(payload.get("synthesis", {})))
    listing_items = _collect_listing_items(payload)
    filter_bar_html = _render_filter_bar(payload, listing_items)
    listing_html = _render_listing_table(listing_items)
    hrefs = report_nav_hrefs(week, at_root=at_root)
    assets = designops_assets_hrefs(at_root=False)
    designops_css_href = assets["css"]
    designops_js_href = assets["js"]
    theme_boot_script = designops_theme_boot_script()
    auth_head_scripts = designops_auth_head_scripts(at_root=False)
    auth_gate_html = designops_auth_gate_html()
    nav_html = report_nav_html(
        week,
        "listing",
        listing_href=hrefs["listing"],
        affinity_href=hrefs["affinity"],
        pipeline_href=hrefs["pipeline"],
        skills_href=hrefs["skills"],
        brand_href=hrefs["brand"],
        usage_href=hrefs.get("usage", "../usage/"),
        personas_href=hrefs.get("personas", "../personas/"),
    )
    report_path_hint = (
        "research-agent/docs/research/research/index.html"
        if at_root
        else f"research-agent/docs/research/reports/{week}.html"
    )
    report_public_url = (
        f"{GITHUB_PAGES_URL}/research/" if (GITHUB_PAGES_URL and at_root)
        else (f"{GITHUB_PAGES_URL}/reports/{week}.html" if GITHUB_PAGES_URL else "")
    )
    workflow_url = github_actions_workflow_url(pages_url=GITHUB_PAGES_URL)
    if at_root:
        page_actions_html = (
            f'<p class="page-actions">'
            f'<a class="view-switch-link" href="{_esc(hrefs["affinity"])}">Open Affinity board →</a>'
            f'<a class="run-workflow-btn run-workflow-admin-only" href="{_esc(workflow_url)}" target="_blank" '
            f'rel="noopener noreferrer" hidden '
            f'title="Sign in to GitHub, then click Run workflow to refresh this report">'
            f"Run Workflow</a>"
            f"</p>"
            f'<p class="run-workflow-hint run-workflow-admin-only muted" hidden>Manual override: sign in to GitHub (repo access required), then click <strong>Run workflow</strong> on the Research Insight Agent page.</p>'
        )
    else:
        page_actions_html = (
            f'<p class="view-switch"><a class="view-switch-link" href="{_esc(hrefs["affinity"])}">'
            f"Open Affinity board →</a></p>"
        )
    voice_cards = collect_user_report_cards(payload, limit=200)
    voice_written = len([
        c for c in voice_cards
        if c["title"].startswith("User said:") or c["title"].startswith("User quote:")
    ])
    voice_studies = len([
        c for c in voice_cards
        if c["title"].startswith("Study feedback:") or c["title"].startswith("Research feedback:")
    ])
    voice_bugs = len([c for c in voice_cards if c["signal"] == "bug"])
    voice_friction = len([c for c in voice_cards if c["signal"] == "friction"])
    voice_dovetail = len([c for c in voice_cards if c["source"] == "dovetail"])
    voice_outset = len([c for c in voice_cards if c["source"] == "outset"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  {theme_boot_script}
  {auth_head_scripts}
  <title>UX Research Monitor — Week of {_esc(week)}</title>
  <link rel="stylesheet" href="{designops_css_href}" />
  <style>
    :root {{ --slideout-width: min(480px, 92vw); }}
    body.slideout-open {{ overflow: hidden; }}
    .stats {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0; }}
    .stat {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; font-size: 0.85rem; }}
    .stat strong {{ font-size: 1.1rem; margin-right: 4px; }}
    .filters {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; margin: 0 0 16px; }}
    .filter-row {{ display: flex; flex-wrap: wrap; gap: 12px; align-items: end; }}
    .filters label {{ display: flex; flex-direction: column; gap: 4px; font-size: 0.78rem; color: var(--muted); font-weight: 500; }}
    .filters select, .filters input, .filter-reset {{ font: inherit; padding: 7px 10px; border-radius: 8px; border: 1px solid var(--border); background: var(--input-bg); color: var(--text); font-size: 0.88rem; }}
    .search-label {{ flex: 1; min-width: 180px; }}
    .search-label input {{ width: 100%; }}
    .filter-reset {{ cursor: pointer; background: var(--bg); font-weight: 500; }}
    .filter-status {{ margin: 10px 0 0; color: var(--muted); font-size: 0.85rem; }}
    .source-counts {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }}
    .pill {{ display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; border: 1px solid var(--border); white-space: nowrap; }}
    .detail-meta {{ margin: 0 0 16px; display: grid; grid-template-columns: 120px 1fr; gap: 6px 12px; font-size: 0.88rem; }}
    .detail-meta dt {{ color: var(--muted); }}
    .detail-meta dd {{ margin: 0; }}
    .table-wrap {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; overflow: auto; }}
    .listing-table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; }}
    .listing-table thead {{ position: sticky; top: 0; z-index: 1; }}
    .listing-table th {{ text-align: left; padding: 10px 14px; font-size: 0.75rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; border-bottom: 1px solid var(--border); white-space: nowrap; }}
    .listing-table td {{ padding: 10px 14px; border-bottom: 1px solid var(--border); vertical-align: top; }}
    .listing-row {{ cursor: pointer; transition: background 0.12s; }}
    .listing-row:focus {{ outline: 2px solid var(--link); outline-offset: -2px; }}
    .listing-row.is-filtered-out {{ display: none; }}
    .cell-finding {{ min-width: 220px; max-width: 420px; }}
    .finding-title {{ font-weight: 600; line-height: 1.35; margin-bottom: 3px; }}
    .finding-sub {{ color: var(--muted); font-size: 0.8rem; line-height: 1.35; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
    .cell-metric {{ color: var(--muted); font-size: 0.82rem; white-space: nowrap; }}
    .cell-date {{ color: var(--muted); font-size: 0.82rem; white-space: nowrap; }}
    .sort-hint {{ color: var(--muted); font-weight: 400; }}
    .badge {{ display: inline-block; padding: 3px 8px; border-radius: 999px; font-size: 0.72rem; font-weight: 600; white-space: nowrap; }}
    .badge-source {{ color: #101828; border: 1px solid rgba(16, 24, 40, 0.12); font-weight: 600; }}
    .badge-status, .badge-type {{ color: #fff; }}
    .is-filtered-out {{ display: none !important; }}
    .hint {{ color: var(--muted); font-size: 0.85rem; margin: 0 0 12px; }}
    .ask-backdrop {{ position: fixed; inset: 0; background: rgba(16,24,40,0.45); z-index: 110; }}
    .ask-backdrop.hidden {{ display: none; }}
    .ask-panel {{
      position: fixed; right: 20px; bottom: 76px; z-index: 111;
      width: min(440px, calc(100vw - 32px)); max-height: min(78vh, 640px);
      background: var(--card); border: 1px solid var(--border); border-radius: 14px;
      box-shadow: var(--fab-shadow);
      display: none; flex-direction: column; overflow: hidden;
    }}
    .ask-panel.open {{ display: flex; }}
    .ask-header {{ padding: 16px 16px 10px; border-bottom: 1px solid var(--border); position: relative; }}
    .ask-header h2 {{ margin: 0 0 4px; font-size: 1.05rem; padding-right: 36px; }}
    .ask-header p {{ margin: 0; color: var(--muted); font-size: 0.84rem; line-height: 1.4; }}
    .ask-body {{ padding: 14px 16px 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }}
    .ask-body label {{ display: flex; flex-direction: column; gap: 4px; font-size: 0.78rem; color: var(--muted); font-weight: 500; }}
    .ask-audience {{ display: flex; gap: 6px; flex-wrap: wrap; }}
    .ask-audience label {{
      flex-direction: row; align-items: center; gap: 6px; margin: 0;
      padding: 7px 12px; border: 1px solid var(--border); border-radius: 8px;
      background: var(--input-bg); color: var(--text); font-size: 0.85rem; font-weight: 500; cursor: pointer;
    }}
    .ask-audience input {{ margin: 0; }}
    .ask-audience label:has(input:checked) {{
      border-color: var(--border-accent); background: var(--info-bg); color: var(--interactive-default);
    }}
    .ask-body textarea {{
      font: inherit; font-size: 0.9rem; padding: 10px 12px; border-radius: 8px;
      border: 1px solid var(--border); resize: vertical; min-height: 72px; background: var(--input-bg); color: var(--text);
    }}
    .ask-mcp-list {{ margin: 0; padding-left: 18px; color: var(--muted); font-size: 0.8rem; }}
    .ask-mcp-list li {{ margin-bottom: 3px; }}
    .ask-mcp-list strong {{ color: var(--text); font-weight: 600; }}
    .ask-actions {{ display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }}
    .ask-copy {{
      border: none; border-radius: 8px; padding: 9px 14px; background: var(--interactive-default); color: #fff;
      font: inherit; font-weight: 600; font-size: 0.88rem; cursor: pointer;
    }}
    .ask-copy:hover {{ background: var(--interactive-hover); }}
    .ask-status {{ margin: 0; color: #067647; font-size: 0.82rem; }}
    .ask-tips {{ margin: 0; padding-left: 18px; color: var(--muted); font-size: 0.8rem; }}
    .ask-tips li {{ margin-bottom: 4px; }}
    .slideout-backdrop {{ position: fixed; inset: 0; background: rgba(16,24,40,0.45); z-index: 1100; opacity: 1; transition: opacity 0.2s; }}
    .slideout-backdrop.hidden {{ display: none; }}
    .slideout {{ position: fixed; top: 0; right: 0; height: 100%; width: var(--slideout-width); background: var(--card); z-index: 1101; box-shadow: -8px 0 32px rgba(16,24,40,0.12); transform: translateX(100%); transition: transform 0.25s ease; display: flex; flex-direction: column; }}
    .slideout.open {{ transform: translateX(0); }}
    .slideout-header {{ padding: 20px 20px 12px; border-bottom: 1px solid var(--border); flex-shrink: 0; }}
    .slideout-header h2 {{ margin: 0 0 6px; font-size: 1.1rem; line-height: 1.35; padding-right: 32px; }}
    .slideout-meta {{ margin: 0; color: var(--muted); font-size: 0.85rem; line-height: 1.4; }}
    .slideout-close {{ position: absolute; top: 16px; right: 16px; width: 32px; height: 32px; border: none; background: var(--bg); border-radius: 8px; cursor: pointer; font-size: 1.2rem; line-height: 1; color: var(--muted); }}
    .slideout-close:hover {{ background: var(--border); }}
    .slideout-body {{ padding: 16px 20px 32px; overflow-y: auto; flex: 1; }}
    .detail-block {{ margin-bottom: 20px; }}
    .detail-block h3 {{ margin: 0 0 8px; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); }}
    .detail-block dl {{ margin: 0; display: grid; grid-template-columns: 120px 1fr; gap: 6px 12px; font-size: 0.88rem; }}
    .detail-block dt {{ color: var(--muted); }}
    .detail-block dd {{ margin: 0; }}
    .ai-block {{ background: var(--ai); border: 1px dashed #c084fc; border-radius: 8px; padding: 12px 14px; }}
    .detail-block ul {{ margin: 0; padding-left: 18px; font-size: 0.88rem; }}
    .detail-block li {{ margin-bottom: 6px; }}
    .detail-links {{ margin-top: 16px; }}
    a {{ color: var(--link); }}
    footer {{ margin-top: 32px; color: var(--muted); font-size: 0.85rem; }}
    template {{ display: none; }}
  </style>
</head>
<body>
  {auth_gate_html}
  {nav_html}
  <div class="wrap">
    <header class="page-header">
      <h1>UX Research Insight Monitor</h1>
      <p class="sub">{_esc(period_label)} ({_esc(period_start)} → {_esc(period_end)}) · {total_items} items · {synthesized} AI analyzed · Generated {_esc(payload.get("generated_at", ""))}</p>
      {page_actions_html}
    </header>

    <aside class="walkthrough-banner is-master">
      <p><strong>Next step.</strong> Take a finding into Cursor with the master skill: <code>use Design Thinking UX</code>. It asks intake questions and invokes Empathize → Test.</p>
      <a href="../skills/#design-thinking-ux">Open design-thinking-ux</a>
    </aside>

    {filter_bar_html}

    <div class="voice-banner" role="note">
      <strong>User reports in this pack:</strong>
      {voice_written} written quotes/comments · {voice_studies} Dovetail/Outset feedback studies ·
      {voice_bugs} bug-tagged · {voice_friction} friction ·
      Dovetail voice {voice_dovetail} · Outset voice {voice_outset} ·
      Freshdesk: {counts.get("freshdesk", 0)}.
      Use Signal → <em>User reports</em> to focus the table.
      See also Affinity <a href="{_esc(hrefs['affinity'])}#user-reports">User reports</a>.
    </div>

    <div class="stats">
      {''.join(f'<div class="stat"><strong>{counts.get(s, 0)}</strong>{SOURCE_LABELS[s]}</div>' for s in SOURCE_ORDER)}
    </div>

    <p class="hint">Click any row to open full details in the slideout panel.</p>

    {listing_html}

    <footer>
      <p>Share this report: bookmark this page or link to your GitHub Pages URL.</p>
    </footer>
  </div>

  <button type="button" id="ask-fab" class="ask-fab" aria-haspopup="dialog" aria-controls="ask-panel"
    data-week-start="{_esc(week)}"
    data-period-label="{_esc(period_label)}"
    data-json-path="research-agent/docs/research/latest.json"
    data-json-url="{_esc(f'{GITHUB_PAGES_URL}/latest.json' if GITHUB_PAGES_URL else '')}"
    data-report-path="{_esc(report_path_hint)}"
    data-report-url="{_esc(report_public_url)}">
    Ask AI
  </button>
  <div id="ask-backdrop" class="ask-backdrop hidden" aria-hidden="true"></div>
  <aside id="ask-panel" class="ask-panel" role="dialog" aria-modal="true" aria-labelledby="ask-title" aria-hidden="true">
    <div class="ask-header">
      <button type="button" id="ask-close" class="slideout-close" aria-label="Close">×</button>
      <h2 id="ask-title">Ask in your AI harness</h2>
      <p>Pick Brand, Partner, or both. The prompt tells your agent to use live MCPs and list what’s connected.</p>
    </div>
    <div class="ask-body">
      <div>
        <div style="font-size:0.78rem;color:var(--muted);font-weight:500;margin-bottom:6px">Audience</div>
        <div class="ask-audience" role="radiogroup" aria-label="Audience scope">
          <label><input type="radio" name="ask-audience" value="brand" /> Brand</label>
          <label><input type="radio" name="ask-audience" value="partner" /> Partner</label>
          <label><input type="radio" name="ask-audience" value="both" checked /> Both</label>
        </div>
      </div>
      <label>
        Your question
        <textarea id="ask-question" rows="3" placeholder="e.g. What’s dropping off in Discover, and do Pendo + Dovetail agree?"></textarea>
      </label>
      <label>
        Prompt preview
        <textarea id="ask-preview" class="ask-preview" rows="8" readonly></textarea>
      </label>
      <div class="ask-actions">
        <button type="button" id="ask-copy" class="ask-copy">Copy prompt</button>
        <p id="ask-status" class="ask-status" aria-live="polite"></p>
      </div>
      <p style="margin:0;font-size:0.78rem;color:var(--muted);font-weight:500">MCPs your harness should have</p>
      <ul class="ask-mcp-list">
        <li><strong>Required:</strong> PostHog, Pendo</li>
        <li><strong>Optional:</strong> Dovetail, Outset (Freshdesk often via the report pack)</li>
        <li>Pack URL: <code>{_esc(f'{GITHUB_PAGES_URL}/latest.json' if GITHUB_PAGES_URL else 'research-agent/docs/research/latest.json')}</code></li>
      </ul>
    </div>
  </aside>

  <div id="slideout-backdrop" class="slideout-backdrop hidden" aria-hidden="true"></div>
  <aside id="slideout" class="slideout" role="dialog" aria-modal="true" aria-labelledby="slideout-title" style="position:fixed">
    <div class="slideout-header" style="position:relative">
      <button type="button" id="slideout-close" class="slideout-close" aria-label="Close">×</button>
      <h2 id="slideout-title">Details</h2>
      <p id="slideout-meta" class="slideout-meta"></p>
    </div>
    <div id="slideout-body" class="slideout-body"></div>
  </aside>

  <script>
    (function () {{
      // Hard-navigate Listing/Affinity — some previews ignore plain relative <a> clicks
      document.querySelectorAll(".report-nav a.nav-link, a.view-switch-link").forEach((a) => {{
        a.addEventListener("click", (e) => {{
          const href = a.getAttribute("href");
          if (!href) return;
          e.preventDefault();
          window.location.assign(href);
        }});
      }});
    }})();
  </script>
  <script src="{designops_js_href}"></script>
{_render_app_script()}
</body>
</html>"""


def _render_user_reports_section(cards: List[Dict[str, Any]]) -> str:
    """Affinity strip for user-reported feedback / bugs / friction / support."""
    if not cards:
        return (
            '<section id="user-reports" class="voice-section">'
            "<h2>User reports</h2>"
            "<p class=\"muted\">No written user feedback, bug notes, friction, or support tickets "
            "in this pack. Freshdesk may be offline; NPS often has theme tags without comments.</p>"
            "</section>"
        )

    by_signal: Dict[str, List[Dict[str, Any]]] = {}
    for card in cards:
        by_signal.setdefault(card.get("signal") or "user_feedback", []).append(card)

    blocks: List[str] = []
    order = ("bug", "user_feedback", "support", "friction")
    for sig in order:
        rows = by_signal.get(sig) or []
        if not rows:
            continue
        cards_html = []
        for card in rows[:12]:
            cards_html.append(
                f'<article class="voice-card signal-{_esc(sig)}">'
                f'<div class="voice-card-top">'
                f'<span class="pill signal signal-{_esc(sig)}">{_esc(SIGNAL_LABELS.get(sig, sig))}</span>'
                f'<span class="src-pill src-{_esc(card.get("source", ""))}">'
                f'{_esc(SOURCE_LABELS.get(card.get("source", ""), card.get("source", "")))}</span>'
                f"</div>"
                f'<h3>{_esc(card.get("title", ""))}</h3>'
                f'<p>{_esc(card.get("subtitle", ""))}</p>'
                f"</article>"
            )
        blocks.append(
            f'<div class="voice-col" data-signal="{_esc(sig)}">'
            f"<h3>{_esc(SIGNAL_LABELS.get(sig, sig))} ({len(rows)})</h3>"
            f'<div class="voice-cards">{"".join(cards_html)}</div></div>'
        )

    return (
        f'<section id="user-reports" class="voice-section">'
        f"<h2>User reports</h2>"
        f"<p class=\"hint\">What users wrote or struggled with — Pendo NPS, Dovetail quotes/highlights, "
        f"Outset feedback studies, support tickets, and friction (rage clicks). "
        f"Separate from PostHog funnel issues below.</p>"
        f'<div class="voice-grid">{"".join(blocks)}</div>'
        f"</section>"
    )


def render_affinity_html_report(payload: Dict[str, Any]) -> str:
    """Themes × Brand/Partner board seeded by PostHog issues + evidence trays."""
    week = payload["week_start"]
    period = payload.get("period", {})
    period_label = period.get("label", "Last 3 months")
    period_start = period.get("start", "")
    period_end = period.get("end", "")
    cards = build_affinity_cards(payload)
    rows = group_affinity_board(cards)
    board_html = render_affinity_board_html(rows)
    high = len([c for c in cards if c.get("severity") == "HIGH"])
    triangulated = len([c for c in cards if c.get("triangulated") or c.get("confidence") != "low"])
    hrefs = report_nav_hrefs(week)
    nav_html = report_nav_html(
        week,
        "affinity",
        listing_href=hrefs["listing"],
        affinity_href=hrefs["affinity"],
        pipeline_href=hrefs["pipeline"],
        skills_href=hrefs["skills"],
        brand_href=hrefs["brand"],
        usage_href=hrefs.get("usage", "../usage/"),
        personas_href=hrefs.get("personas", "../personas/"),
    )
    voice_cards = collect_user_report_cards(payload, limit=48)
    voice_html = _render_user_reports_section(voice_cards)
    assets = designops_assets_hrefs(at_root=False)
    designops_css_href = assets["css"]
    designops_js_href = assets["js"]
    theme_boot_script = designops_theme_boot_script()
    auth_head_scripts = designops_auth_head_scripts(at_root=False)
    auth_gate_html = designops_auth_gate_html()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  {theme_boot_script}
  {auth_head_scripts}
  <title>UX Affinity — Week of {_esc(week)}</title>
  <link rel="stylesheet" href="{designops_css_href}" />
  <style>
    :root {{ --slideout-width: min(480px, 92vw); }}
    body.slideout-open {{ overflow: hidden; }}
    .wrap {{ max-width: 1400px; padding-bottom: 80px; }}
    .page-header {{ margin-bottom: 16px; }}
    .stats {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0; }}
    .stat {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; font-size: 0.85rem; }}
    .stat strong {{ font-size: 1.1rem; margin-right: 4px; }}
    .hint {{ color: var(--muted); font-size: 0.85rem; margin: 0 0 16px; }}
    .voice-section {{ border-radius: 12px; padding: 16px; margin: 0 0 28px; }}
    .voice-section h2 {{ margin: 0 0 6px; font-size: 1.15rem; }}
    .voice-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-top: 12px; }}
    .voice-cards {{ display: flex; flex-direction: column; gap: 8px; }}
    .voice-card-top {{ display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 6px; }}
    .voice-card h3 {{ margin: 0 0 4px; font-size: 0.88rem; line-height: 1.35; }}
    .voice-card p {{ margin: 0; font-size: 0.78rem; color: var(--muted); line-height: 1.35; }}
    .pill {{ display: inline-block; padding: 2px 7px; border-radius: 6px; font-size: 0.7rem; font-weight: 600; border: 1px solid var(--border); }}
    .aff-theme {{ margin-bottom: 28px; }}
    .aff-theme-title {{ margin: 0 0 12px; font-size: 1.15rem; font-weight: 700; }}
    .aff-theme-title .count, .aff-col-title .count {{ color: var(--muted); font-weight: 500; font-size: 0.9em; }}
    .aff-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }}
    @media (max-width: 960px) {{ .aff-grid {{ grid-template-columns: 1fr; }} }}
    .aff-col {{ background: var(--background-hover); border-radius: 12px; padding: 10px; min-height: 80px; }}
    .aff-col-title {{ margin: 0 0 10px; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); }}
    .aff-col-cards {{ display: flex; flex-direction: column; gap: 10px; }}
    .col-empty {{ margin: 0; color: var(--muted); font-size: 0.85rem; text-align: center; padding: 12px 0; }}
    .aff-card {{
      background: var(--card); border: 1px solid var(--border); border-radius: 10px;
      padding: 12px 14px; cursor: pointer; transition: box-shadow 0.12s, border-color 0.12s;
    }}
    .aff-card:hover, .aff-card:focus {{ border-color: var(--border-accent); box-shadow: var(--elevation-xs); outline: none; }}
    .aff-card-head {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-bottom: 8px; }}
    .aff-card-title {{ margin: 0 0 6px; font-size: 0.95rem; line-height: 1.35; }}
    .aff-card-metric {{ margin: 0 0 4px; font-size: 0.85rem; font-weight: 600; color: var(--pill-bug-text); }}
    .aff-card-area {{ margin: 0 0 8px; font-size: 0.78rem; color: var(--muted); }}
    .aff-card-sources {{ display: flex; flex-wrap: wrap; gap: 4px; align-items: center; }}
    .src-pill {{ display: inline-block; padding: 2px 7px; border-radius: 999px; font-size: 0.7rem; font-weight: 600; border: 1px solid var(--border); }}
    .ev-count {{ font-size: 0.72rem; color: var(--muted); margin-left: 4px; }}
    .sev-badge {{ display: inline-block; padding: 2px 8px; border-radius: 999px; color: #fff; font-size: 0.7rem; font-weight: 700; }}
    .conf-badge {{ font-size: 0.72rem; font-weight: 600; text-transform: capitalize; }}
    .filters {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; margin-bottom: 16px; display: flex; flex-wrap: wrap; gap: 12px; align-items: end; }}
    .filters label {{ display: flex; flex-direction: column; gap: 4px; font-size: 0.78rem; color: var(--muted); font-weight: 500; }}
    .filters select {{ font: inherit; padding: 7px 10px; border-radius: 8px; border: 1px solid var(--border); background: var(--input-bg); color: var(--text); }}
    .aff-card.is-filtered-out, .aff-theme.is-filtered-out {{ display: none; }}
    .slideout-backdrop {{ position: fixed; inset: 0; background: rgba(16,24,40,0.45); z-index: 1100; }}
    .slideout-backdrop.hidden {{ display: none; }}
    .slideout {{ position: fixed; top: 0; right: 0; height: 100%; width: var(--slideout-width); background: var(--card); z-index: 1101; box-shadow: -8px 0 32px rgba(16,24,40,0.12); transform: translateX(100%); transition: transform 0.25s ease; display: flex; flex-direction: column; }}
    .slideout.open {{ transform: translateX(0); }}
    .slideout-header {{ padding: 20px 20px 12px; border-bottom: 1px solid var(--border); position: relative; }}
    .slideout-header h2 {{ margin: 0 0 6px; font-size: 1.1rem; line-height: 1.35; padding-right: 32px; }}
    .slideout-meta {{ margin: 0; color: var(--muted); font-size: 0.85rem; }}
    .slideout-close {{ position: absolute; top: 16px; right: 16px; width: 32px; height: 32px; border: none; background: var(--bg); border-radius: 8px; cursor: pointer; font-size: 1.2rem; color: var(--muted); }}
    .slideout-body {{ padding: 16px 20px 32px; overflow-y: auto; flex: 1; }}
    .detail-block {{ margin-bottom: 20px; }}
    .detail-block h3 {{ margin: 0 0 8px; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); }}
    .detail-meta {{ margin: 0 0 16px; display: grid; grid-template-columns: 120px 1fr; gap: 6px 12px; font-size: 0.88rem; }}
    .detail-meta dt {{ color: var(--muted); }} .detail-meta dd {{ margin: 0; }}
    .ai-block {{ background: var(--ai); border: 1px dashed #c084fc; border-radius: 8px; padding: 12px 14px; }}
    .ev-list {{ margin: 0; padding: 0; list-style: none; }}
    .ev-item {{ padding: 10px 0; border-bottom: 1px solid var(--border); font-size: 0.88rem; }}
    .ev-snip {{ color: var(--muted); font-size: 0.82rem; margin-top: 4px; }}
    .muted {{ color: var(--muted); }}
    a {{ color: var(--link); }}
    template {{ display: none; }}
  </style>
</head>
<body>
  {auth_gate_html}
  {nav_html}
  <div class="wrap">
    <header class="page-header">
      <h1>UX Affinity Board</h1>
      <p class="sub">{_esc(period_label)} ({_esc(period_start)} → {_esc(period_end)}) · PostHog issue spine · Themes × Brand/Partner</p>
      <p class="view-switch"><a class="view-switch-link" href="{_esc(hrefs['listing'])}">← Back to Listing</a></p>
    </header>

    <aside class="walkthrough-banner is-master">
      <p><strong>Next step.</strong> Clustered themes here are Empathize input. Start a guided run with the master skill: <code>use Design Thinking UX</code>.</p>
      <a href="../skills/#design-thinking-ux">Open design-thinking-ux</a>
    </aside>

    <div class="stats">
      <div class="stat"><strong>{len(cards)}</strong> issues</div>
      <div class="stat"><strong>{high}</strong> high severity</div>
      <div class="stat"><strong>{triangulated}</strong> multi-source</div>
      <div class="stat"><strong>{len(rows)}</strong> themes</div>
    </div>

    <section class="filters" aria-label="Filter affinity board">
      <label>Audience
        <select id="aff-filter-audience">
          <option value="all">All</option>
          <option value="Brand">Brand</option>
          <option value="Partner">Partner</option>
          <option value="Shared">Shared</option>
        </select>
      </label>
      <label>Severity
        <select id="aff-filter-severity">
          <option value="all">All</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
        </select>
      </label>
      <label>Confidence
        <select id="aff-filter-confidence">
          <option value="all">All</option>
          <option value="high">High</option>
          <option value="medium">Medium+</option>
        </select>
      </label>
    </section>

    <p class="hint">Each sticky below is a PostHog funnel issue. User-written feedback and bugs are in the section above.</p>

    {voice_html}

    {board_html}
  </div>

  <a class="ask-fab" href="{_esc(hrefs['listing'])}">Ask AI on Listing →</a>

  <div id="slideout-backdrop" class="slideout-backdrop hidden" aria-hidden="true"></div>
  <aside id="slideout" class="slideout" role="dialog" aria-modal="true" aria-labelledby="slideout-title">
    <div class="slideout-header">
      <button type="button" id="slideout-close" class="slideout-close" aria-label="Close">×</button>
      <h2 id="slideout-title">Issue</h2>
      <p id="slideout-meta" class="slideout-meta"></p>
    </div>
    <div id="slideout-body" class="slideout-body"></div>
  </aside>

  <script>
    (function () {{
      document.querySelectorAll(".report-nav a.nav-link, a.view-switch-link, a.ask-fab").forEach((a) => {{
        a.addEventListener("click", (e) => {{
          const href = a.getAttribute("href");
          if (!href || href.startsWith("#")) return;
          e.preventDefault();
          window.location.assign(href);
        }});
      }});

      const audienceEl = document.getElementById("aff-filter-audience");
      const severityEl = document.getElementById("aff-filter-severity");
      const confidenceEl = document.getElementById("aff-filter-confidence");
      const backdrop = document.getElementById("slideout-backdrop");
      const slideout = document.getElementById("slideout");
      const slideoutTitle = document.getElementById("slideout-title");
      const slideoutMeta = document.getElementById("slideout-meta");
      const slideoutBody = document.getElementById("slideout-body");
      const slideoutClose = document.getElementById("slideout-close");

      function matches(card) {{
        const aud = audienceEl.value;
        const sev = severityEl.value;
        const conf = confidenceEl.value;
        if (aud !== "all" && card.dataset.audience !== aud) return false;
        if (sev !== "all" && card.dataset.severity !== sev) return false;
        if (conf === "high" && card.dataset.confidence !== "high") return false;
        if (conf === "medium") {{
          const c = card.dataset.confidence;
          if (c !== "high" && c !== "medium") return false;
        }}
        return true;
      }}

      function applyFilters() {{
        document.querySelectorAll(".aff-theme").forEach((theme) => {{
          let visible = 0;
          theme.querySelectorAll(".aff-card").forEach((card) => {{
            const show = matches(card);
            card.classList.toggle("is-filtered-out", !show);
            if (show) visible += 1;
          }});
          theme.classList.toggle("is-filtered-out", visible === 0);
        }});
      }}

      function openCard(card) {{
        const id = card.dataset.cardId;
        const tmpl = document.getElementById("aff-detail-" + id);
        if (!tmpl) return;
        slideoutTitle.textContent = card.querySelector(".aff-card-title").textContent;
        slideoutMeta.textContent = card.querySelector(".aff-card-metric").textContent;
        slideoutBody.innerHTML = tmpl.innerHTML;
        backdrop.classList.remove("hidden");
        slideout.classList.add("open");
        document.body.classList.add("slideout-open");
      }}

      function close() {{
        backdrop.classList.add("hidden");
        slideout.classList.remove("open");
        document.body.classList.remove("slideout-open");
        slideoutBody.innerHTML = "";
      }}

      document.querySelector(".wrap").addEventListener("click", (e) => {{
        const card = e.target.closest(".aff-card");
        if (card && !card.classList.contains("is-filtered-out")) openCard(card);
      }});
      document.querySelector(".wrap").addEventListener("keydown", (e) => {{
        if (e.key !== "Enter" && e.key !== " ") return;
        const card = e.target.closest(".aff-card");
        if (card) {{ e.preventDefault(); openCard(card); }}
      }});
      slideoutClose.addEventListener("click", close);
      backdrop.addEventListener("click", close);
      document.addEventListener("keydown", (e) => {{ if (e.key === "Escape") close(); }});
      [audienceEl, severityEl, confidenceEl].forEach((el) => el.addEventListener("change", applyFilters));
      applyFilters();
    }})();
  </script>
  <script src="{designops_js_href}"></script>
</body>
</html>"""


def publish_github_pages_report(payload: Dict[str, Any], docs_root: Optional[Path] = None) -> Optional[str]:
    """Write HTML + JSON report files. Returns public URL if GITHUB_PAGES_URL is set.

    Latest listing is written as docs/research/research/index.html.
    Site home (pipeline) at docs/research/index.html is not overwritten.
    Archive copies remain under docs/research/reports/{week}.html.
    """
    root = docs_root or DOCS_ROOT
    reports_dir = root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    week = payload["week_start"]
    report_html = render_html_report(payload, at_root=False)
    index_html = render_html_report(payload, at_root=True)
    affinity_html = render_affinity_html_report(payload)
    report_json = json.dumps(payload, indent=2, default=str)

    html_path = reports_dir / f"{week}.html"
    affinity_path = reports_dir / f"{week}-affinity.html"
    json_path = reports_dir / f"{week}.json"
    html_path.write_text(report_html, encoding="utf-8")
    affinity_path.write_text(affinity_html, encoding="utf-8")
    json_path.write_text(report_json, encoding="utf-8")

    index_path = root / "research" / "index.html"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(index_html, encoding="utf-8")

    latest_path = root / "latest.json"
    latest_path.write_text(report_json, encoding="utf-8")

    print(f"  ✅ GitHub Pages listing: {index_path}")
    print(f"  ✅ Archive listing: {html_path}")
    print(f"  ✅ Affinity board: {affinity_path}")
    if GITHUB_PAGES_URL:
        public_url = f"{GITHUB_PAGES_URL}/research/"
        print(f"  🔗 Public URL: {public_url}")
        print(f"  🔗 Affinity URL: {GITHUB_PAGES_URL}/reports/{week}-affinity.html")
        return public_url

    print(f"  ℹ️  Set GITHUB_PAGES_URL to emit a shareable link")
    return str(index_path)
