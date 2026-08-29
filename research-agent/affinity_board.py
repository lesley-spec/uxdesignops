"""Affinity board: PostHog issue spine on a Themes × Brand/Partner grid."""

from __future__ import annotations

import html
import os
import re
from pathlib import Path
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


def designops_assets_hrefs(
    *, at_root: bool = False, skills_page: bool = False, pack_page: bool = False
) -> Dict[str, str]:
    """Shared CSS/JS paths for GitHub Pages."""
    if at_root:
        prefix = "./shared"
    elif pack_page:
        prefix = "../../../shared"
    elif skills_page:
        prefix = "../shared"
    else:
        prefix = "../shared"
    return {
        "css": f"{prefix}/designops.css",
        "js": f"{prefix}/designops-theme.js",
        "auth_config": f"{prefix}/auth-config.js",
        "auth_js": f"{prefix}/designops-auth.js",
    }


def designops_auth_head_scripts(
    *, at_root: bool = False, skills_page: bool = False, pack_page: bool = False
) -> str:
    assets = designops_assets_hrefs(at_root=at_root, skills_page=skills_page, pack_page=pack_page)
    return (
        f'<script src="{assets["auth_config"]}"></script>'
        f'<script src="https://accounts.google.com/gsi/client" async defer></script>'
        f'<script src="{assets["auth_js"]}" defer></script>'
    )


def designops_auth_gate_html() -> str:
    domain = "impact.com"
    return (
        f'<div id="designops-auth-gate" class="designops-auth-screen" role="dialog" '
        f'aria-modal="true" aria-labelledby="designops-auth-title">'
        f'<div class="designops-auth-card">'
        f'<h1 id="designops-auth-title">UX DesignOps</h1>'
        f'<p>Sign in with your <strong>@{domain}</strong> Google account to view this site.</p>'
        f'<div id="designops-google-signin"></div>'
        f'<p id="designops-auth-status"></p>'
        f"</div></div>"
        f'<div id="designops-auth-denied" class="designops-auth-screen" hidden role="alert">'
        f'<div class="designops-auth-card">'
        f'<h1 class="designops-auth-denied-title">You don\u2019t have permission to view this</h1>'
        f'<p>This site is restricted to <strong>@{domain}</strong> Google accounts '
        f"(for example lesley@{domain}).</p>"
        f'<p id="designops-auth-status-denied"></p>'
        f"</div></div>"
    )


def designops_theme_boot_script() -> str:
    """Inline script — matches partner-prototype next-themes (class=dark on html)."""
    return (
        "<script>"
        "(function(){try{"
        'var k="theme",s=localStorage.getItem(k),d;'
        'if(s==="dark")d=true;else if(s==="light")d=false;'
        'else d=window.matchMedia("(prefers-color-scheme: dark)").matches;'
        "var e=document.documentElement;"
        'if(d)e.classList.add("dark");else e.classList.remove("dark");'
        'e.style.colorScheme=d?"dark":"light";'
        "}catch(x){}})();"
        "</script>"
    )


def theme_toggle_html() -> str:
    """Moon/sun icon toggle — same pattern as partner-prototype ThemeToggle."""
    return (
        '<button type="button" class="theme-toggle" id="theme-toggle" '
        'aria-label="Toggle theme">'
        '<svg class="theme-icon theme-icon-moon" viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'
        "</svg>"
        '<svg class="theme-icon theme-icon-sun" viewBox="0 0 24 24" aria-hidden="true">'
        '<circle cx="12" cy="12" r="4"/>'
        '<path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>'
        "</svg>"
        "</button>"
    )


def impact_logo_markup() -> str:
    """Inline impact wordmark so currentColor follows light/dark theme."""
    logo_path = Path(__file__).resolve().parent / "docs" / "research" / "shared" / "impact-logo.svg"
    svg = logo_path.read_text(encoding="utf-8").strip()
    svg = svg.replace(
        'role="img" aria-label="impact"',
        'class="top-nav-logo" width="98" height="32" aria-hidden="true" focusable="false"',
    )
    return svg


def top_nav_brand_html(brand_href: str) -> str:
    return (
        f'<a class="top-nav-brand" href="{_esc(brand_href)}">'
        f"{impact_logo_markup()}"
        f'<span class="top-nav-brand-text">UX DesignOps</span></a>'
    )


def report_nav_html(
    week: str,
    active: str,
    *,
    listing_href: str = "",
    affinity_href: str = "",
    skills_href: str = "",
    pipeline_href: str = "",
    brand_href: str = "",
) -> str:
    """Top bar: Design Thinking Pipeline (home) | Research | Affinity | Skills."""
    listing = listing_href or f"./{week}.html"
    affinity = affinity_href or f"./{week}-affinity.html"
    skills = skills_href or "../skills/"
    pipeline = pipeline_href or "../"
    brand = brand_href or pipeline
    return (
        f'<header class="top-nav" role="banner">'
        f'<div class="top-nav-inner">'
        f"{top_nav_brand_html(brand)}"
        f'<div class="top-nav-actions">'
        f'<nav class="report-nav" aria-label="Site sections">'
        f'<a class="nav-link{" is-active" if active == "pipeline" else ""}" '
        f'href="{_esc(pipeline)}" data-nav="pipeline">Design Thinking Pipeline</a>'
        f'<a class="nav-link{" is-active" if active == "listing" else ""}" '
        f'href="{_esc(listing)}" data-nav="listing">Research</a>'
        f'<a class="nav-link{" is-active" if active == "affinity" else ""}" '
        f'href="{_esc(affinity)}" data-nav="affinity">Affinity</a>'
        f'<a class="nav-link{" is-active" if active == "skills" else ""}" '
        f'href="{_esc(skills)}" data-nav="skills">Skills</a>'
        f"</nav>"
        f"{theme_toggle_html()}"
        f"</div>"
        f"</div>"
        f"</header>"
    )


def github_actions_workflow_url(
    workflow_file: str = "research-agent.yml",
    *,
    pages_url: str = "",
    require_login: bool = True,
) -> str:
    """Link to GitHub Actions workflow page for manual workflow_dispatch runs."""
    base = (
        pages_url
        or os.environ.get("GITHUB_PAGES_URL", "")
        or "https://lesley-spec.github.io/uxdesignops"
    ).rstrip("/")
    match = re.match(r"https?://([^.]+)\.github\.io/([^/]+)", base)
    if match:
        owner, repo = match.group(1), match.group(2)
        workflow_url = f"https://github.com/{owner}/{repo}/actions/workflows/{workflow_file}"
    else:
        workflow_url = f"https://github.com/lesley-spec/uxdesignops/actions/workflows/{workflow_file}"

    if not require_login:
        return workflow_url

    from urllib.parse import quote
    return f"https://github.com/login?return_to={quote(workflow_url, safe='')}"


def report_nav_hrefs(week: str, *, at_root: bool = False, page: str = "") -> Dict[str, str]:
    """Relative nav links for report HTML.

    page:
      pipeline — site home (docs/research/index.html)
      research — latest listing (docs/research/research/index.html)
      reports  — archive + affinity (docs/research/reports/)

    at_root=True is kept as an alias for page="research" (listing is no longer
    the GitHub Pages homepage).
    """
    loc = page or ("research" if at_root else "reports")
    if loc == "pipeline":
        return {
            "pipeline": "./",
            "listing": "./research/",
            "affinity": f"./reports/{week}-affinity.html",
            "skills": "./skills/",
            "brand": "./",
        }
    if loc == "research":
        return {
            "pipeline": "../",
            "listing": "./",
            "affinity": f"../reports/{week}-affinity.html",
            "skills": "../skills/",
            "brand": "../",
        }
    return {
        "pipeline": "../",
        "listing": "../research/",
        "affinity": f"./{week}-affinity.html",
        "skills": "../skills/",
        "brand": "../",
    }
