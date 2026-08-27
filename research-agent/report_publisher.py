"""Publish research agent output as linkable GitHub Pages HTML + JSON."""

from __future__ import annotations

import html
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DOCS_ROOT = Path(os.environ.get("REPORT_OUTPUT_DIR", "docs/research"))
GITHUB_PAGES_URL = os.environ.get("GITHUB_PAGES_URL", "").rstrip("/")


def _esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def _severity_badge(severity: str) -> str:
    color = "#d32f2f" if severity == "HIGH" else "#f57c00"
    return f'<span class="badge" style="background:{color}">{_esc(severity)}</span>'


def _render_research_list(context: Dict[str, Any]) -> str:
    items: List[str] = []

    for item in context.get("pendo_feedback", []):
        items.append(
            f'<li class="verified"><strong>Pendo</strong> ({_esc(item.get("guide_name", "Guide"))}): '
            f'"{_esc(item.get("response", ""))}"</li>'
        )

    for item in context.get("dovetail_insights", []):
        title = _esc(item.get("title", "Untitled"))
        link = item.get("url")
        if link:
            items.append(f'<li class="verified"><strong>Dovetail</strong>: <a href="{_esc(link)}">{title}</a></li>')
        else:
            items.append(f'<li class="verified"><strong>Dovetail</strong>: {title}</li>')

    for item in context.get("freshdesk_tickets", []):
        subject = _esc(item.get("subject", "Support ticket"))
        body_preview = _esc((item.get("body") or "")[:240])
        link = item.get("url")
        meta = _esc(item.get("ticket_type") or item.get("status") or "Freshdesk")
        if link:
            items.append(
                f'<li class="verified"><strong>Freshdesk</strong> ({meta}): '
                f'<a href="{_esc(link)}">{subject}</a><br/><em>{body_preview}</em></li>'
            )
        else:
            items.append(
                f'<li class="verified"><strong>Freshdesk</strong> ({meta}): {subject}<br/><em>{body_preview}</em></li>'
            )

    for item in context.get("outset_studies", []):
        items.append(
            f'<li class="verified"><strong>Outset</strong>: {_esc(item.get("title", "Untitled"))}</li>'
        )

    if not items:
        return "<li>No related qualitative research found.</li>"
    return "\n".join(items)


def build_report_payload(
    *,
    week_start: str,
    issues: List[Dict[str, Any]],
    synthesis: Dict[str, str],
    pendo_feedback: List[Dict[str, Any]],
    dovetail_insights: List[Dict[str, Any]],
    freshdesk_tickets: List[Dict[str, Any]],
    outset_studies: List[Dict[str, Any]],
    confluence_weekly_report: Optional[str] = None,
) -> Dict[str, Any]:
    high = len([i for i in issues if i.get("severity") == "HIGH"])
    medium = len([i for i in issues if i.get("severity") == "MEDIUM"])
    enriched = len([
        i for i in issues
        if any(i.get("research_context", {}).get(key) for key in (
            "pendo_feedback", "dovetail_insights", "freshdesk_tickets", "outset_studies"
        ))
    ])

    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "week_start": week_start,
        "summary": {
            "issues_found": len(issues),
            "high_severity": high,
            "medium_severity": medium,
            "issues_with_research_context": enriched,
            "pendo_feedback_count": len(pendo_feedback),
            "dovetail_insights_count": len(dovetail_insights),
            "freshdesk_tickets_count": len(freshdesk_tickets),
            "outset_studies_count": len(outset_studies),
        },
        "sources": {
            "posthog": True,
            "pendo": bool(pendo_feedback),
            "dovetail": bool(dovetail_insights),
            "freshdesk": bool(freshdesk_tickets),
            "outset": bool(outset_studies),
        },
        "confluence_weekly_report": confluence_weekly_report,
        "issues": issues,
        "synthesis": synthesis,
        "pendo_feedback": pendo_feedback[:20],
        "dovetail_insights": dovetail_insights[:20],
        "freshdesk_tickets": freshdesk_tickets[:20],
    }


def _render_issue_cards(issues: List[Dict[str, Any]], synthesis: Dict[str, str]) -> str:
    if not issues:
        return '<p class="empty">No significant funnel drop-offs detected this week.</p>'

    cards = []
    for issue in issues:
        title = issue.get("title", "Untitled issue")
        analysis = synthesis.get(title, "Analysis pending.")
        context = issue.get("research_context", {})
        cards.append(
            f"""
            <article class="issue-card">
              <header>
                <h3>{_esc(title)}</h3>
                {_severity_badge(issue.get("severity", "MEDIUM"))}
              </header>
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
        )
    return "\n".join(cards)


def _render_unmatched_research(
    freshdesk_tickets: List[Dict[str, Any]],
    pendo_feedback: List[Dict[str, Any]],
    dovetail_insights: List[Dict[str, Any]],
) -> str:
    sections = []

    if freshdesk_tickets:
        items = "".join(
            f"<li class=\"verified\"><strong>{_esc(t.get('subject', 'Ticket'))}</strong> "
            f"({_esc(t.get('status', ''))}) — {_esc((t.get('body') or '')[:180])}</li>"
            for t in freshdesk_tickets[:15]
        )
        sections.append(f"<h2>Freshdesk support signals (last 7 days)</h2><ul>{items}</ul>")

    if pendo_feedback:
        items = "".join(
            f"<li class=\"verified\"><strong>{_esc(p.get('guide_name', 'Guide'))}</strong>: "
            f"\"{_esc(p.get('response', ''))}\"</li>"
            for p in pendo_feedback[:10]
        )
        sections.append(f"<h2>Pendo feedback</h2><ul>{items}</ul>")

    if dovetail_insights:
        items = "".join(
            f"<li class=\"verified\">{_esc(d.get('title', 'Insight'))}</li>"
            for d in dovetail_insights[:10]
        )
        sections.append(f"<h2>Dovetail research</h2><ul>{items}</ul>")

    return "\n".join(sections)


def render_html_report(payload: Dict[str, Any]) -> str:
    summary = payload["summary"]
    week = payload["week_start"]
    confluence_link = payload.get("confluence_weekly_report")
    confluence_html = (
        f'<p><a href="{_esc(confluence_link)}">View Confluence weekly report</a></p>'
        if confluence_link else ""
    )

    research_signals_html = _render_unmatched_research(
        payload.get("freshdesk_tickets", []),
        payload.get("pendo_feedback", []),
        payload.get("dovetail_insights", []),
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>UX Research Monitor — Week of { _esc(week) }</title>
  <style>
    :root {{
      --bg: #fafafa; --card: #fff; --text: #1a1a1a; --muted: #666;
      --verified: #e8f5e9; --ai: #fce4ec; --border: #e0e0e0; --link: #1565c0;
    }}
    body {{ font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; background: var(--bg); color: var(--text); }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 32px 20px 64px; }}
    header {{ margin-bottom: 32px; }}
    h1 {{ margin: 0 0 8px; font-size: 2rem; }}
    .sub {{ color: var(--muted); margin: 0; }}
    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 24px 0; }}
    .stat {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 16px; }}
    .stat strong {{ display: block; font-size: 1.6rem; }}
    .legend {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 16px 0 28px; }}
    .pill {{ padding: 6px 12px; border-radius: 999px; font-size: 0.85rem; border: 1px solid var(--border); }}
    .pill.verified {{ background: var(--verified); }}
    .pill.ai {{ background: var(--ai); border-style: dashed; }}
    .issue-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 16px; }}
    .issue-card header {{ display: flex; justify-content: space-between; gap: 12px; align-items: start; }}
    .badge {{ color: #fff; padding: 4px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: 700; }}
    .metrics {{ display: flex; flex-wrap: wrap; gap: 16px; margin: 12px 0; color: var(--muted); }}
    .analysis {{ background: var(--ai); border: 1px dashed #f48fb1; border-radius: 8px; padding: 12px 14px; margin: 12px 0; }}
    .analysis h4, .research h4 {{ margin: 0 0 8px; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.04em; }}
    li.verified {{ background: var(--verified); margin-bottom: 8px; padding: 8px 10px; border-radius: 6px; list-style: none; }}
    a {{ color: var(--link); }}
    footer {{ margin-top: 40px; color: var(--muted); font-size: 0.9rem; }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>UX Research Insight Monitor</h1>
      <p class="sub">Week of {_esc(week)} · Generated {_esc(payload.get("generated_at", ""))}</p>
      {confluence_html}
    </header>

    <section class="stats">
      <div class="stat"><strong>{summary["issues_found"]}</strong> issues found</div>
      <div class="stat"><strong>{summary["high_severity"]}</strong> high severity</div>
      <div class="stat"><strong>{summary["issues_with_research_context"]}</strong> with research context</div>
      <div class="stat"><strong>{summary["freshdesk_tickets_count"]}</strong> Freshdesk tickets</div>
      <div class="stat"><strong>{summary["pendo_feedback_count"]}</strong> Pendo responses</div>
      <div class="stat"><strong>{summary["dovetail_insights_count"]}</strong> Dovetail items</div>
    </section>

    <div class="legend">
      <span class="pill verified">Verified data (PostHog, Pendo, Dovetail, Freshdesk)</span>
      <span class="pill ai">AI-generated analysis</span>
    </div>

    <section>
      {_render_issue_cards(payload.get("issues", []), payload.get("synthesis", {}))}
    </section>

    <section>
      {research_signals_html}
    </section>

    <footer>
      <p>Share this report: bookmark this page or link to your GitHub Pages URL.</p>
    </footer>
  </div>
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
