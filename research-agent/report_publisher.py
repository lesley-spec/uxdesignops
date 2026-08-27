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
    group_by_audience_and_theme,
    tag_issues,
    tag_research_items,
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
    for issue in payload.get("issues", []):
        if issue.get("theme"):
            themes.add(str(issue["theme"]))
    for key in ("pendo_feedback", "dovetail_insights", "freshdesk_tickets", "outset_studies"):
        for item in payload.get(key, []):
            if item.get("theme"):
                themes.add(str(item["theme"]))
    return sorted(themes)


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
        "Ticket": "#c2185b",
    }
    color = colors.get(label, "#757575")
    if label in ("HIGH", "MEDIUM"):
        return f'<span class="badge badge-status" style="background:{color}">{_esc(label)}</span>'
    return f'<span class="badge badge-type" style="background:{color}">{_esc(label)}</span>'


def _item_date_sort_key(iso_date: str) -> str:
    """Normalize ISO timestamps for descending sort (empty dates sort last)."""
    return (iso_date or "").strip()


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
        idx += 1
        items.append(kwargs)

    for issue in payload.get("posthog_dropoffs", payload.get("issues", [])):
        title = issue.get("title", "Untitled")
        users = issue.get("users_affected", 0)
        users_display = f"{int(users):,}" if isinstance(users, (int, float)) else str(users)
        add(
            id=f"posthog-{idx}",
            source="posthog",
            title=title,
            subtitle=issue.get("step", ""),
            audience=issue.get("audience", ""),
            theme=issue.get("theme", ""),
            severity=issue.get("severity", ""),
            status=issue.get("severity", ""),
            metric=f"{issue.get('drop_percentage', 0)}% drop · {users_display} users",
            date=issue.get("created_at") or posthog_date,
            search_text=f"{title} {issue.get('funnel_name', '')} {issue.get('step', '')}".lower(),
            detail_kind="posthog",
            detail_data={"issue": issue, "analysis": synthesis.get(title, "")},
        )

    type_labels = {"insight": "Insight", "highlight": "Highlight", "note": "Note"}
    for item in payload.get("dovetail_insights", []):
        title = item.get("title") or "Untitled"
        body = item.get("body") or item.get("preview") or ""
        item_type = type_labels.get(item.get("type", ""), item.get("type", "Note"))
        add(
            source="dovetail",
            title=title,
            subtitle=(body[:120] + "…") if len(body) > 120 else body,
            audience=item.get("audience", ""),
            theme=item.get("theme", ""),
            severity="",
            status=item_type,
            metric=item.get("project_title") or "—",
            date=item.get("created_at", ""),
            search_text=f"{title} {body}".lower(),
            detail_kind="dovetail",
            detail_data={"item": item},
        )

    for item in payload.get("outset_studies", []):
        title = item.get("title") or "Untitled study"
        summary = item.get("summary") or item.get("body") or ""
        add(
            source="outset",
            title=title,
            subtitle=(summary[:120] + "…") if len(summary) > 120 else summary,
            audience=item.get("audience", ""),
            theme=item.get("theme", ""),
            severity="",
            status="Study",
            metric=item.get("interview_method") or "—",
            date=item.get("created_at", ""),
            search_text=f"{title} {summary}".lower(),
            detail_kind="outset",
            detail_data={"item": item},
        )

    for item in payload.get("pendo_analytics", []):
        title = item.get("title") or "Pendo analytics"
        subtitle = item.get("subtitle") or item.get("body") or ""
        add(
            source="pendo",
            title=title,
            subtitle=subtitle,
            audience=item.get("audience", ""),
            theme=item.get("theme", ""),
            severity="HIGH" if item.get("type") == "Friction" else "",
            status=item.get("type") or "Page",
            metric=item.get("metric") or "—",
            date=str(item.get("created_at") or item.get("timestamp") or ""),
            search_text=f"{title} {subtitle}".lower(),
            detail_kind="pendo_analytics",
            detail_data={"item": item},
        )

    for item in payload.get("pendo_feedback", []):
        title = item.get("guide_name") or item.get("title") or "Pendo guide"
        response = item.get("response") or item.get("subtitle") or ""
        add(
            source="pendo",
            title=title,
            subtitle=(response[:120] + "…") if len(response) > 120 else response,
            audience=item.get("audience", ""),
            theme=item.get("theme", ""),
            severity="",
            status="Feedback",
            metric=item.get("metric") or item.get("poll_type") or "—",
            date=str(item.get("timestamp") or item.get("created_at") or ""),
            search_text=f"{title} {response}".lower(),
            detail_kind="pendo",
            detail_data={"item": item},
        )

    for item in payload.get("freshdesk_tickets", []):
        title = item.get("subject") or "Support ticket"
        body = item.get("body") or ""
        add(
            source="freshdesk",
            title=title,
            subtitle=(body[:120] + "…") if len(body) > 120 else body,
            audience=item.get("audience", ""),
            theme=item.get("theme", ""),
            severity="",
            status=item.get("status") or item.get("ticket_type") or "Ticket",
            metric="—",
            date=str(item.get("created_at") or ""),
            search_text=f"{title} {body}".lower(),
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
        return (
            f'<section class="detail-block"><h3>Response</h3>'
            f"<p>{_esc(d.get('response', ''))}</p></section>"
            f"<dl>"
            f"<dt>Guide</dt><dd>{_esc(d.get('guide_name') or d.get('title', ''))}</dd>"
            f"<dt>Poll type</dt><dd>{_esc(d.get('poll_type') or '—')}</dd>"
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
        theme = item.get("theme") or "—"
        templates.append(
            f'<template id="detail-{row_id}">'
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
            f'data-severity="{_esc(item.get("severity", ""))}" '
            f'data-date="{_esc(item.get("date", ""))}" '
            f'data-search-text="{_esc(item.get("search_text", ""))}">'
            f'<td class="cell-date">{_esc(date_display)}</td>'
            f"<td>{_source_badge(item['source'])}</td>"
            f'<td class="cell-finding">'
            f'<div class="finding-title">{_esc(item["title"])}</div>'
            f'<div class="finding-sub">{_esc(item.get("subtitle", ""))}</div>'
            f"</td>"
            f'<td><span class="pill audience">{_esc(audience)}</span></td>'
            f'<td><span class="pill theme">{_esc(theme)}</span></td>'
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
        f"<th>Source</th><th>Finding</th><th>Audience</th>"
        f"<th>Theme</th><th>Status</th><th>Metric</th>"
        f"</tr></thead>"
        f'<tbody id="listing-body">{"".join(rows)}</tbody>'
        f"</table></div>"
    )


def _render_filter_bar(payload: Dict[str, Any]) -> str:
    theme_options = "".join(
        f'<option value="{_esc(theme)}">{_esc(theme)}</option>'
        for theme in _collect_themes(payload)
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
          Theme
          <select id="filter-theme">
            <option value="all">All themes</option>
            {theme_options}
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
      const severityEl = document.getElementById("filter-severity");
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
        const severity = severityEl.value;
        const source = sourceEl.value;
        const itemAudience = el.dataset.audience || "";
        const itemTheme = el.dataset.theme || "";
        const itemSeverity = el.dataset.severity || "";
        const itemSource = el.dataset.source || "";
        const searchText = el.dataset.searchText || "";

        if (source !== "all" && itemSource !== source) return false;
        if (audience !== "all" && itemAudience !== audience) return false;
        if (theme !== "all" && itemTheme !== theme) return false;
        if (severity !== "all" && itemSeverity && itemSeverity !== severity) return false;
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
        if (themeEl.value !== "all") parts.push(themeEl.value);
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
      document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeSlideout();
      });

      [sourceEl, audienceEl, themeEl, severityEl].forEach((el) => {
        el.addEventListener("change", applyFilters);
      });
      searchEl.addEventListener("input", applyFilters);
      resetEl.addEventListener("click", () => {
        sourceEl.value = "all";
        audienceEl.value = "all";
        themeEl.value = "all";
        severityEl.value = "all";
        searchEl.value = "";
        applyFilters();
      });

      applyFilters();
    })();
  </script>
"""


def render_html_report(payload: Dict[str, Any]) -> str:
    summary = payload["summary"]
    week = payload["week_start"]
    period = payload.get("period", {})
    period_label = period.get("label", "Last 3 months")
    period_start = period.get("start", "")
    period_end = period.get("end", "")
    counts = payload.get("source_counts", {})
    total_items = sum(counts.values())
    synthesized = summary.get("ai_synthesized_count", len(payload.get("synthesis", {})))
    filter_bar_html = _render_filter_bar(payload)
    listing_items = _collect_listing_items(payload)
    listing_html = _render_listing_table(listing_items)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>UX Research Monitor — Week of {_esc(week)}</title>
  <style>
    :root {{
      --bg: #f4f5f7; --card: #fff; --text: #1a1a1a; --muted: #667085;
      --verified: #e8f5e9; --ai: #f3e8ff; --border: #e4e7ec; --link: #175cd3;
      --slideout-width: min(480px, 92vw);
    }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; background: var(--bg); color: var(--text); }}
    body.slideout-open {{ overflow: hidden; }}
    .wrap {{ max-width: 1280px; margin: 0 auto; padding: 24px 20px 48px; }}
    header {{ margin-bottom: 20px; }}
    h1 {{ margin: 0 0 6px; font-size: 1.75rem; font-weight: 700; }}
    .sub {{ color: var(--muted); margin: 0; font-size: 0.92rem; }}
    .stats {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0; }}
    .stat {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; font-size: 0.85rem; }}
    .stat strong {{ font-size: 1.1rem; margin-right: 4px; }}
    .filters {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; margin: 0 0 16px; }}
    .filter-row {{ display: flex; flex-wrap: wrap; gap: 12px; align-items: end; }}
    .filters label {{ display: flex; flex-direction: column; gap: 4px; font-size: 0.78rem; color: var(--muted); font-weight: 500; }}
    .filters select, .filters input, .filter-reset {{ font: inherit; padding: 7px 10px; border-radius: 8px; border: 1px solid var(--border); background: #fff; font-size: 0.88rem; }}
    .search-label {{ flex: 1; min-width: 180px; }}
    .search-label input {{ width: 100%; }}
    .filter-reset {{ cursor: pointer; background: var(--bg); font-weight: 500; }}
    .filter-status {{ margin: 10px 0 0; color: var(--muted); font-size: 0.85rem; }}
    .source-counts {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }}
    .pill {{ display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; border: 1px solid var(--border); white-space: nowrap; }}
    .pill.audience {{ background: #eff8ff; color: #175cd3; border-color: #b2ddff; }}
    .pill.theme {{ background: #f9f5ff; color: #6941c6; border-color: #e9d7fe; }}
    .pill.source-pill {{ background: #fff; }}
    .table-wrap {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; overflow: auto; }}
    .listing-table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; }}
    .listing-table thead {{ background: #f9fafb; position: sticky; top: 0; z-index: 1; }}
    .listing-table th {{ text-align: left; padding: 10px 14px; font-size: 0.75rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; border-bottom: 1px solid var(--border); white-space: nowrap; }}
    .listing-table td {{ padding: 10px 14px; border-bottom: 1px solid var(--border); vertical-align: top; }}
    .listing-row {{ cursor: pointer; transition: background 0.12s; }}
    .listing-row:hover {{ background: #f9fafb; }}
    .listing-row:focus {{ outline: 2px solid var(--link); outline-offset: -2px; }}
    .listing-row.is-filtered-out {{ display: none; }}
    .cell-finding {{ min-width: 220px; max-width: 420px; }}
    .finding-title {{ font-weight: 600; line-height: 1.35; margin-bottom: 3px; }}
    .finding-sub {{ color: var(--muted); font-size: 0.8rem; line-height: 1.35; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
    .cell-metric {{ color: var(--muted); font-size: 0.82rem; white-space: nowrap; }}
    .cell-date {{ color: var(--muted); font-size: 0.82rem; white-space: nowrap; }}
    .sort-hint {{ color: var(--muted); font-weight: 400; }}
    .badge {{ display: inline-block; padding: 3px 8px; border-radius: 999px; font-size: 0.72rem; font-weight: 600; white-space: nowrap; }}
    .badge-source {{ color: #344054; border: 1px solid var(--border); }}
    .badge-status, .badge-type {{ color: #fff; }}
    .is-filtered-out {{ display: none !important; }}
    .hint {{ color: var(--muted); font-size: 0.85rem; margin: 0 0 12px; }}
    .slideout-backdrop {{ position: fixed; inset: 0; background: rgba(16,24,40,0.45); z-index: 100; opacity: 1; transition: opacity 0.2s; }}
    .slideout-backdrop.hidden {{ display: none; }}
    .slideout {{ position: fixed; top: 0; right: 0; height: 100%; width: var(--slideout-width); background: var(--card); z-index: 101; box-shadow: -8px 0 32px rgba(16,24,40,0.12); transform: translateX(100%); transition: transform 0.25s ease; display: flex; flex-direction: column; }}
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
  <div class="wrap">
    <header>
      <h1>UX Research Insight Monitor</h1>
      <p class="sub">{_esc(period_label)} ({_esc(period_start)} → {_esc(period_end)}) · {total_items} items · {synthesized} AI analyzed · Generated {_esc(payload.get("generated_at", ""))}</p>
    </header>

    {filter_bar_html}

    <div class="stats">
      {''.join(f'<div class="stat"><strong>{counts.get(s, 0)}</strong>{SOURCE_LABELS[s]}</div>' for s in SOURCE_ORDER)}
    </div>

    <p class="hint">Click any row to open full details in the slideout panel.</p>

    {listing_html}

    <footer>
      <p>Share this report: bookmark this page or link to your GitHub Pages URL.</p>
    </footer>
  </div>

  <div id="slideout-backdrop" class="slideout-backdrop hidden" aria-hidden="true"></div>
  <aside id="slideout" class="slideout" role="dialog" aria-modal="true" aria-labelledby="slideout-title" style="position:fixed">
    <div class="slideout-header" style="position:relative">
      <button type="button" id="slideout-close" class="slideout-close" aria-label="Close">×</button>
      <h2 id="slideout-title">Details</h2>
      <p id="slideout-meta" class="slideout-meta"></p>
    </div>
    <div id="slideout-body" class="slideout-body"></div>
  </aside>

{_render_app_script()}
</body>
</html>"""


def render_index_html(reports: List[str], latest_week: str) -> str:
    links = "\n".join(
        f'<li><a href="reports/{_esc(week)}.html">Week of {_esc(week)}</a></li>'
        for week in sorted(reports, reverse=True)
    )
    latest_href = f"reports/{latest_week}.html" if latest_week else "#"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="refresh" content="0; url={_esc(latest_href)}" />
  <title>UX Research Monitor</title>
</head>
<body>
  <p>Redirecting to the latest report… <a href="{_esc(latest_href)}">Week of {_esc(latest_week)}</a></p>
  <h2>Archive</h2>
  <ul>{links}</ul>
</body>
</html>"""


def publish_github_pages_report(payload: Dict[str, Any], docs_root: Optional[Path] = None) -> Optional[str]:
    """Write HTML + JSON report files. Returns public URL if GITHUB_PAGES_URL is set."""
    root = docs_root or DOCS_ROOT
    reports_dir = root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    week = payload["week_start"]
    report_html = render_html_report(payload)
    report_json = json.dumps(payload, indent=2, default=str)

    html_path = reports_dir / f"{week}.html"
    json_path = reports_dir / f"{week}.json"
    html_path.write_text(report_html, encoding="utf-8")
    json_path.write_text(report_json, encoding="utf-8")

    existing_weeks = sorted({p.stem for p in reports_dir.glob("*.html")})
    index_path = root / "index.html"
    index_path.write_text(render_index_html(existing_weeks, week), encoding="utf-8")

    latest_path = root / "latest.json"
    latest_path.write_text(report_json, encoding="utf-8")

    print(f"  ✅ GitHub Pages report: {html_path}")
    if GITHUB_PAGES_URL:
        public_url = f"{GITHUB_PAGES_URL}/reports/{week}.html"
        print(f"  🔗 Public URL: {public_url}")
        return public_url

    print(f"  ℹ️  Set GITHUB_PAGES_URL to emit a shareable link")
    return str(html_path)
