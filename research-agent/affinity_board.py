"""Affinity board: PostHog issue spine on a Themes × Brand/Partner grid."""

from __future__ import annotations

import html
from typing import Any, Dict, List

from issue_taxonomy import (
    AUDIENCE_ORDER,
    THEME_RULES,
    classify_product_area,
    classify_theme,
    classify_audience,
)

SOURCE_LABELS = {
    "posthog": "PostHog",
    "pendo": "Pendo",
    "dovetail": "Dovetail",
    "freshdesk": "Freshdesk",
    "outset": "Outset",
}

THEME_ORDER = [theme for theme, _, _ in THEME_RULES] + [
    "Brand Experience",
    "Partner Experience",
    "Cross-audience",
]

EVIDENCE_CAP = 8
ANALYTICS_MATCH_CAP = 4


def _esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def _confidence(source_keys: List[str]) -> str:
    n = len(set(source_keys))
    if n >= 3:
        return "high"
    if n >= 2:
        return "medium"
    return "low"


def _evidence_from_context(issue: Dict[str, Any]) -> List[Dict[str, Any]]:
    context = issue.get("research_context") or {}
    out: List[Dict[str, Any]] = []

    for item in context.get("pendo_feedback") or []:
        out.append({
            "source": "pendo",
            "kind": "Feedback",
            "title": item.get("guide_name") or item.get("title") or "Pendo feedback",
            "snippet": (item.get("response") or "")[:160],
            "url": item.get("url") or "",
        })

    for item in context.get("dovetail_insights") or []:
        out.append({
            "source": "dovetail",
            "kind": (item.get("type") or "note").title(),
            "title": item.get("title") or "Dovetail item",
            "snippet": (item.get("body") or item.get("preview") or "")[:160],
            "url": item.get("url") or "",
        })

    for item in context.get("outset_studies") or []:
        out.append({
            "source": "outset",
            "kind": "Study",
            "title": item.get("title") or "Outset study",
            "snippet": (item.get("summary") or item.get("body") or "")[:160],
            "url": item.get("url") or "",
        })

    for item in context.get("freshdesk_tickets") or []:
        out.append({
            "source": "freshdesk",
            "kind": "Ticket",
            "title": item.get("subject") or "Support ticket",
            "snippet": (item.get("body") or "")[:160],
            "url": item.get("url") or "",
        })

    return out


def _match_pendo_analytics(
    issue: Dict[str, Any],
    analytics: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Attach Pendo pages/features/friction in the same theme or product area."""
    theme = issue.get("theme") or ""
    audience = issue.get("audience") or ""
    product_area = issue.get("product_area") or classify_product_area(issue)
    matches: List[Dict[str, Any]] = []

    for item in analytics:
        item_theme = item.get("theme") or classify_theme({
            "funnel_name": item.get("title", ""),
            "title": item.get("title", ""),
            "audience": item.get("audience") or classify_audience({
                "funnel_name": item.get("title", ""),
                "title": item.get("title", ""),
            }),
        })
        item_area = item.get("product_area") or classify_product_area({
            "funnel_name": item.get("title", ""),
            "title": item.get("title", ""),
            "audience": item.get("audience", ""),
        })
        item_audience = item.get("audience") or ""

        theme_hit = theme and item_theme == theme
        area_hit = product_area and item_area == product_area
        audience_ok = (
            not item_audience
            or item_audience == audience
            or item_audience == "Shared"
            or audience == "Shared"
        )
        if not audience_ok:
            continue
        if not (theme_hit or area_hit):
            continue

        matches.append({
            "source": "pendo",
            "kind": item.get("type") or "Page",
            "title": item.get("title") or "Pendo entity",
            "snippet": item.get("subtitle") or item.get("metric") or "",
            "url": "",
            "metric": item.get("metric") or "",
        })
        if len(matches) >= ANALYTICS_MATCH_CAP:
            break

    return matches


def build_affinity_cards(
    payload: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """One card per PostHog drop-off, with attached multi-source evidence."""
    synthesis = payload.get("synthesis") or {}
    analytics = payload.get("pendo_analytics") or []
    issues = payload.get("posthog_dropoffs") or payload.get("issues") or []
    cards: List[Dict[str, Any]] = []

    for idx, issue in enumerate(issues):
        audience = issue.get("audience") or classify_audience(issue)
        theme = issue.get("theme") or classify_theme({**issue, "audience": audience})
        product_area = issue.get("product_area") or classify_product_area({
            **issue,
            "audience": audience,
            "theme": theme,
        })

        evidence = _evidence_from_context(issue)
        seen = {(e["source"], e["title"]) for e in evidence}
        for extra in _match_pendo_analytics(
            {**issue, "audience": audience, "theme": theme, "product_area": product_area},
            analytics,
        ):
            key = (extra["source"], extra["title"])
            if key in seen:
                continue
            seen.add(key)
            evidence.append(extra)

        evidence = evidence[:EVIDENCE_CAP]
        source_keys = ["posthog"] + [e["source"] for e in evidence]
        title = issue.get("funnel_name") or issue.get("title") or "Untitled issue"
        drop = issue.get("drop_percentage", 0)
        users = issue.get("users_affected", 0)
        analysis = synthesis.get(issue.get("title", ""), "") or synthesis.get(title, "")

        cards.append({
            "id": f"issue-{idx}",
            "title": title,
            "problem": f"{drop}% drop" + (
                f" · {int(users):,} users" if isinstance(users, (int, float)) else ""
            ),
            "step": issue.get("step", ""),
            "severity": issue.get("severity", "MEDIUM"),
            "audience": audience,
            "theme": theme,
            "product_area": product_area,
            "drop_percentage": drop,
            "users_affected": users,
            "posthog_link": issue.get("posthog_link", ""),
            "analysis": analysis if analysis and analysis != "Analysis pending." else "",
            "evidence": evidence,
            "source_keys": sorted(set(source_keys)),
            "confidence": _confidence(source_keys),
            "triangulated": bool((issue.get("research_context") or {}).get("triangulated"))
            or len(set(source_keys)) >= 3,
        })

    cards.sort(
        key=lambda c: (
            c.get("severity") != "HIGH",
            -float(c.get("drop_percentage") or 0),
            -int(c.get("users_affected") or 0),
        )
    )
    return cards


def group_affinity_board(
    cards: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Themes × audiences; skip empty theme rows."""
    by_theme: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
    for card in cards:
        theme = card.get("theme") or "Cross-audience"
        audience = card.get("audience") or "Shared"
        by_theme.setdefault(theme, {a: [] for a in AUDIENCE_ORDER})
        if audience not in by_theme[theme]:
            by_theme[theme][audience] = []
        by_theme[theme][audience].append(card)

    theme_rank = {t: i for i, t in enumerate(THEME_ORDER)}
    rows: List[Dict[str, Any]] = []
    for theme in sorted(by_theme.keys(), key=lambda t: theme_rank.get(t, 999)):
        cols = by_theme[theme]
        total = sum(len(cols.get(a, [])) for a in AUDIENCE_ORDER)
        if total == 0:
            continue
        rows.append({
            "theme": theme,
            "total": total,
            "columns": {a: cols.get(a, []) for a in AUDIENCE_ORDER},
        })
    return rows


def _source_pills(source_keys: List[str]) -> str:
    return "".join(
        f'<span class="src-pill src-{_esc(s)}">{_esc(SOURCE_LABELS.get(s, s))}</span>'
        for s in source_keys
    )


def _confidence_badge(level: str) -> str:
    colors = {"high": "#067647", "medium": "#b54708", "low": "#667085"}
    return (
        f'<span class="conf-badge" style="color:{colors.get(level, "#667085")}">'
        f"{_esc(level)} confidence</span>"
    )


def _severity_badge(severity: str) -> str:
    color = "#d32f2f" if severity == "HIGH" else "#f57c00"
    return f'<span class="sev-badge" style="background:{color}">{_esc(severity)}</span>'


def _render_evidence_list(evidence: List[Dict[str, Any]]) -> str:
    if not evidence:
        return '<p class="muted">No attached qualitative evidence yet — use Ask AI / MCP to dig deeper.</p>'
    items = []
    for e in evidence:
        link = ""
        if e.get("url"):
            link = (
                f' <a href="{_esc(e["url"])}" target="_blank" rel="noopener">Open</a>'
            )
        items.append(
            f'<li class="ev-item">'
            f'<span class="src-pill src-{_esc(e.get("source", ""))}">'
            f'{_esc(SOURCE_LABELS.get(e.get("source", ""), e.get("source", "")))}</span> '
            f'<strong>{_esc(e.get("title", ""))}</strong> '
            f'<span class="muted">({_esc(e.get("kind", ""))})</span>'
            f'<div class="ev-snip">{_esc(e.get("snippet", ""))}</div>'
            f"{link}</li>"
        )
    return f'<ul class="ev-list">{"".join(items)}</ul>'


def _render_issue_card(card: Dict[str, Any]) -> str:
    cid = card["id"]
    analysis = card.get("analysis") or ""
    analysis_html = (
        f'<section class="detail-block ai-block"><h3>AI analysis</h3>'
        f"<p>{_esc(analysis)}</p></section>"
        if analysis
        else ""
    )
    posthog = card.get("posthog_link") or "#"
    template = (
        f'<template id="aff-detail-{cid}">'
        f'<dl class="detail-meta">'
        f"<dt>Product area</dt><dd>{_esc(card.get('product_area', ''))}</dd>"
        f"<dt>Theme</dt><dd>{_esc(card.get('theme', ''))}</dd>"
        f"<dt>Audience</dt><dd>{_esc(card.get('audience', ''))}</dd>"
        f"<dt>Confidence</dt><dd>{_esc(card.get('confidence', ''))}</dd>"
        f"</dl>"
        f'<section class="detail-block"><h3>Funnel step</h3>'
        f"<p>{_esc(card.get('step', '') or '—')}</p></section>"
        f"{analysis_html}"
        f'<section class="detail-block"><h3>Evidence tray</h3>'
        f"{_render_evidence_list(card.get('evidence') or [])}</section>"
        f'<p class="detail-links"><a href="{_esc(posthog)}" target="_blank" rel="noopener">'
        f"Open in PostHog</a></p>"
        f"</template>"
    )
    ev_count = len(card.get("evidence") or [])
    return (
        f"{template}"
        f'<article class="aff-card" tabindex="0" role="button" data-card-id="{cid}" '
        f'data-audience="{_esc(card.get("audience", ""))}" '
        f'data-theme="{_esc(card.get("theme", ""))}" '
        f'data-severity="{_esc(card.get("severity", ""))}" '
        f'data-confidence="{_esc(card.get("confidence", ""))}">'
        f'<header class="aff-card-head">'
        f"{_severity_badge(card.get('severity', ''))}"
        f"{_confidence_badge(card.get('confidence', 'low'))}"
        f"</header>"
        f'<h3 class="aff-card-title">{_esc(card.get("title", ""))}</h3>'
        f'<p class="aff-card-metric">{_esc(card.get("problem", ""))}</p>'
        f'<p class="aff-card-area">{_esc(card.get("product_area", ""))}</p>'
        f'<div class="aff-card-sources">{_source_pills(card.get("source_keys") or [])}'
        f'<span class="ev-count">{ev_count} evidence</span></div>'
        f"</article>"
    )


def render_affinity_board_html(rows: List[Dict[str, Any]]) -> str:
    if not rows:
        return '<p class="empty">No PostHog issues to map.</p>'

    sections: List[str] = []
    for row in rows:
        cols_html = []
        for audience in AUDIENCE_ORDER:
            cards = row["columns"].get(audience) or []
            cards_html = (
                "".join(_render_issue_card(c) for c in cards)
                if cards
                else '<p class="col-empty">—</p>'
            )
            cols_html.append(
                f'<div class="aff-col" data-audience="{_esc(audience)}">'
                f'<h3 class="aff-col-title">{_esc(audience)} '
                f'<span class="count">({len(cards)})</span></h3>'
                f'<div class="aff-col-cards">{cards_html}</div></div>'
            )
        sections.append(
            f'<section class="aff-theme" data-theme="{_esc(row["theme"])}">'
            f'<h2 class="aff-theme-title">{_esc(row["theme"])} '
            f'<span class="count">({row["total"]})</span></h2>'
            f'<div class="aff-grid">{"".join(cols_html)}</div>'
            f"</section>"
        )
    return "\n".join(sections)


def report_nav_html(
    week: str,
    active: str,
    *,
    listing_href: str = "",
    affinity_href: str = "",
) -> str:
    """Top bar with Listing | Affinity. Prefer explicit hrefs from caller."""
    listing = listing_href or f"./{week}.html"
    affinity = affinity_href or f"./{week}-affinity.html"
    return (
        f'<header class="top-nav" role="banner">'
        f'<div class="top-nav-inner">'
        f'<a class="top-nav-brand" href="{_esc(listing)}">UX Research Monitor</a>'
        f'<nav class="report-nav" aria-label="Report views">'
        f'<a class="nav-link{" is-active" if active == "listing" else ""}" '
        f'href="{_esc(listing)}" data-nav="listing">Listing</a>'
        f'<a class="nav-link{" is-active" if active == "affinity" else ""}" '
        f'href="{_esc(affinity)}" data-nav="affinity">Affinity</a>'
        f"</nav>"
        f"</div>"
        f"</header>"
    )


def report_nav_hrefs(week: str, *, at_root: bool = False) -> Dict[str, str]:
    """Relative nav links for report HTML.

    at_root=True: listing lives at docs/research/index.html (GitHub Pages home).
    at_root=False: listing + affinity live under docs/research/reports/.
    """
    if at_root:
        return {
            "listing": "./",
            "affinity": f"./reports/{week}-affinity.html",
        }
    return {
        "listing": f"./{week}.html",
        "affinity": f"./{week}-affinity.html",
    }
