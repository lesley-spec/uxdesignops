"""Parse and classify user-reported voice (feedback, bugs, friction, support)."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

# Signal types surfaced in the report UI
SIGNAL_USER_FEEDBACK = "user_feedback"
SIGNAL_FRICTION = "friction"
SIGNAL_BUG = "bug"
SIGNAL_SUPPORT = "support"
SIGNAL_QUANT = "quant"
SIGNAL_RESEARCH = "research"

SIGNAL_LABELS = {
    SIGNAL_USER_FEEDBACK: "User feedback",
    SIGNAL_FRICTION: "Friction",
    SIGNAL_BUG: "Bug report",
    SIGNAL_SUPPORT: "Support",
    SIGNAL_QUANT: "Quant drop-off",
    SIGNAL_RESEARCH: "Research",
}

BUG_KEYWORDS = (
    "bug",
    "broken",
    "error",
    "crash",
    "not work",
    "doesn't work",
    "does not work",
    "can't",
    "cannot",
    "unable to",
    "stuck",
    "fail",
    "failed",
    "glitch",
    "incorrect",
    "wrong",
    "missing credit",
    "not showing",
    "past bug",
)

NOISE_COMMENTS = {"", "dsds", ".", "..", "n/a", "na", "none", "test"}


def parse_nps_response(response: str) -> Dict[str, Any]:
    """Parse Pendo NPSReason payloads: THEMES:a,b|COMMENT:text|FOLLOWUP:Yes."""
    themes: List[str] = []
    comment = ""
    followup = ""
    raw = (response or "").strip()
    if not raw:
        return {"themes": themes, "comment": comment, "followup": followup, "raw": raw}

    if "THEMES:" in raw.upper() or "COMMENT:" in raw.upper():
        for part in raw.split("|"):
            part = part.strip()
            upper = part.upper()
            if upper.startswith("THEMES:"):
                themes = [t.strip() for t in part.split(":", 1)[1].split(",") if t.strip()]
            elif upper.startswith("COMMENT:"):
                comment = part.split(":", 1)[1].strip()
            elif upper.startswith("FOLLOWUP:"):
                followup = part.split(":", 1)[1].strip()
    else:
        comment = raw

    return {"themes": themes, "comment": comment, "followup": followup, "raw": raw}


def is_meaningful_comment(comment: str) -> bool:
    c = (comment or "").strip()
    if c.lower() in NOISE_COMMENTS:
        return False
    if len(c) < 8:
        return False
    # repeated single token junk
    if len(set(c.lower())) <= 2:
        return False
    return True


def looks_like_bug(text: str, *, strict: bool = False) -> bool:
    blob = (text or "").lower()
    if strict:
        strong = (
            "bug", "broken", "error", "crash", "not work", "doesn't work",
            "does not work", "glitch", "past bug", "stuck loading",
            "not showing", "missing credit", "working api",
        )
        return any(k in blob for k in strong)
    return any(k in blob for k in BUG_KEYWORDS)


def classify_feedback_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich a Pendo feedback row with parsed comment + signal."""
    parsed = parse_nps_response(item.get("response") or item.get("body") or "")
    comment = parsed["comment"]
    themes = parsed["themes"]
    meaningful = is_meaningful_comment(comment)
    signal = SIGNAL_BUG if looks_like_bug(comment, strict=True) else SIGNAL_USER_FEEDBACK

    if meaningful:
        title = f"User said: {_short(comment, 90)}"
        subtitle = ("NPS themes: " + ", ".join(themes)) if themes else "In-app NPS / poll feedback"
    elif themes:
        title = f"NPS themes: {', '.join(themes[:4])}"
        subtitle = "No written comment — theme tags only"
    else:
        title = f"In-app feedback: {item.get('guide_name') or 'Pendo'}"
        subtitle = "Empty or low-signal poll response"
        signal = SIGNAL_USER_FEEDBACK

    return {
        **parsed,
        "meaningful": meaningful,
        "signal": signal,
        "display_title": title,
        "display_subtitle": subtitle,
    }


VOICE_TITLE_HINTS = (
    "feedback",
    "nps",
    "survey",
    "interview",
    "inquiry",
    "user requested",
    "pain",
    "complaint",
    "experience",
)

QUOTE_HINTS = (
    " i ",
    " i'm ",
    " we ",
    " you guys",
    " need to",
    " wish",
    " like it",
    " don't",
    " doesn't",
    " can't",
    " unfortunately",
    " frustrat",
    " difficult",
    " confusing",
    " should look",
    " user requested",
)


def is_dovetail_user_voice(item: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Return (is_voice, kind) for Dovetail items.
    kind: bug | quote | feedback_note
    """
    title = (item.get("title") or "").strip()
    body = (item.get("body") or item.get("preview") or "").strip()
    item_type = (item.get("type") or "").lower()
    blob = f"{title} {body[:400]}".lower()

    # Prefer quote classification for highlights; only strict bug wording → bug
    if looks_like_bug(title, strict=True) or looks_like_bug(blob, strict=True):
        return True, "bug"

    title_l = title.lower()
    if any(h in title_l for h in ("feedback", "nps", "survey", "user requested")):
        return True, "feedback_note"

    if item_type == "highlight" and len(body) >= 40:
        padded = f" {body.lower()} "
        if any(h in padded for h in QUOTE_HINTS) or body[:1].islower() or body.startswith(("I ", "We ", "You ")):
            return True, "quote"
        if len(body) >= 80:
            return True, "quote"

    if item_type == "insight" and any(h in blob for h in VOICE_TITLE_HINTS):
        return True, "feedback_note"

    return False, ""


def is_outset_user_voice(item: Dict[str, Any]) -> bool:
    title = (item.get("title") or "").lower()
    summary = (item.get("summary") or item.get("body") or "").lower()
    if not title or title == "untitled study" or title == "test data":
        return False
    if any(h in title for h in VOICE_TITLE_HINTS):
        return True
    if any(h in title for h in ("marketplace", "reporting", "recruitment", "mcp", "lightning", "feeds")):
        # Product discovery / experience studies
        if any(w in summary for w in ("feedback", "experience", "survey", "interview", "learn about")):
            return True
    if "feedback" in summary or "share your" in summary:
        return True
    return False


def classify_listing_signal(
    *,
    source: str,
    status: str = "",
    title: str = "",
    body: str = "",
    item_type: str = "",
    item: Dict[str, Any] | None = None,
) -> str:
    blob = f"{title} {body} {status} {item_type}".lower()
    if source == "freshdesk" or status.lower() == "ticket":
        return SIGNAL_SUPPORT
    if item_type == "Friction" or status == "Friction":
        return SIGNAL_FRICTION
    if source == "pendo" and (status == "Feedback" or item_type == "Feedback"):
        return SIGNAL_BUG if looks_like_bug(blob) else SIGNAL_USER_FEEDBACK
    if source == "posthog":
        return SIGNAL_QUANT

    if source == "dovetail":
        ok, kind = is_dovetail_user_voice(item or {"title": title, "body": body, "type": item_type})
        if ok:
            return SIGNAL_BUG if kind == "bug" else SIGNAL_USER_FEEDBACK
        return SIGNAL_RESEARCH

    if source == "outset":
        if looks_like_bug(blob):
            return SIGNAL_BUG
        if is_outset_user_voice(item or {"title": title, "summary": body, "body": body}):
            return SIGNAL_USER_FEEDBACK
        return SIGNAL_RESEARCH

    if looks_like_bug(blob):
        return SIGNAL_BUG
    if source == "pendo":
        return SIGNAL_FRICTION if "friction" in blob else SIGNAL_USER_FEEDBACK
    return SIGNAL_RESEARCH


def _short(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def collect_user_report_cards(payload: Dict[str, Any], *, limit: int = 60) -> List[Dict[str, Any]]:
    """Standalone affinity stickies for user-reported voice (not PostHog spine)."""
    cards: List[Dict[str, Any]] = []

    for idx, item in enumerate(payload.get("pendo_feedback") or []):
        meta = classify_feedback_item(item)
        if not meta["meaningful"] and not meta["themes"]:
            continue
        if not meta["meaningful"] and not any(
            t in {"Performance & Reliability", "Ease of Use", "Payments", "Tracking"}
            for t in meta["themes"]
        ):
            continue
        cards.append({
            "id": f"voice-pendo-{idx}",
            "signal": meta["signal"],
            "source": "pendo",
            "title": meta["display_title"],
            "subtitle": meta["display_subtitle"],
            "audience": item.get("audience") or "Shared",
            "theme": item.get("theme") or (" · ".join(meta["themes"][:2]) if meta["themes"] else "Cross-audience"),
            "product_area": item.get("product_area") or "Cross-platform",
            "date": item.get("created_at") or item.get("timestamp") or "",
            "severity": "HIGH" if meta["signal"] == SIGNAL_BUG else "MEDIUM",
            "evidence_snippet": meta["comment"] or ", ".join(meta["themes"]),
            "raw": item,
        })

    for idx, item in enumerate(payload.get("pendo_analytics") or []):
        if (item.get("type") or "") != "Friction":
            continue
        cards.append({
            "id": f"voice-friction-{idx}",
            "signal": SIGNAL_FRICTION,
            "source": "pendo",
            "title": f"Friction: {item.get('title') or 'Page'}",
            "subtitle": item.get("subtitle") or item.get("metric") or "Rage / dead clicks",
            "audience": item.get("audience") or "Shared",
            "theme": item.get("theme") or "Cross-audience",
            "product_area": item.get("product_area") or "Cross-platform",
            "date": item.get("created_at") or "",
            "severity": "HIGH",
            "evidence_snippet": item.get("metric") or "",
            "raw": item,
        })

    for idx, item in enumerate(payload.get("freshdesk_tickets") or []):
        cards.append({
            "id": f"voice-fd-{idx}",
            "signal": SIGNAL_SUPPORT,
            "source": "freshdesk",
            "title": f"Support: {item.get('subject') or 'Ticket'}",
            "subtitle": (item.get("body") or "")[:140],
            "audience": item.get("audience") or "Shared",
            "theme": item.get("theme") or "Cross-audience",
            "product_area": item.get("product_area") or "Cross-platform",
            "date": item.get("created_at") or "",
            "severity": "MEDIUM",
            "evidence_snippet": item.get("body") or "",
            "raw": item,
        })

    for idx, item in enumerate(payload.get("dovetail_insights") or []):
        ok, kind = is_dovetail_user_voice(item)
        if not ok:
            continue
        title = (item.get("title") or "Untitled").strip()
        body = (item.get("body") or item.get("preview") or "").strip()
        if kind == "bug":
            signal = SIGNAL_BUG
            display_title = f"Bug note: {_short(title, 90)}"
            subtitle = _short(body, 140) or "Dovetail bug / issue note"
        elif kind == "quote":
            signal = SIGNAL_USER_FEEDBACK
            quote = body or title
            display_title = f"User quote: {_short(quote, 90)}"
            subtitle = f"Dovetail {(item.get('type') or 'highlight')} · {_short(title, 80)}" if body else "Dovetail highlight"
        else:
            signal = SIGNAL_USER_FEEDBACK
            display_title = f"Research feedback: {_short(title, 90)}"
            subtitle = _short(body, 140) or "Dovetail feedback / NPS note"

        cards.append({
            "id": f"voice-dv-{idx}",
            "signal": signal,
            "source": "dovetail",
            "title": display_title,
            "subtitle": subtitle,
            "audience": item.get("audience") or "Shared",
            "theme": item.get("theme") or "Cross-audience",
            "product_area": item.get("product_area") or "Cross-platform",
            "date": item.get("created_at") or "",
            "severity": "HIGH" if signal == SIGNAL_BUG else "MEDIUM",
            "evidence_snippet": body[:240] or title,
            "raw": item,
        })

    for idx, item in enumerate(payload.get("outset_studies") or []):
        if not is_outset_user_voice(item):
            continue
        title = (item.get("title") or "Untitled study").strip()
        summary = (item.get("summary") or item.get("body") or "").strip()
        method = item.get("interview_method") or "Study"
        signal = SIGNAL_BUG if looks_like_bug(f"{title} {summary[:200]}") else SIGNAL_USER_FEEDBACK
        cards.append({
            "id": f"voice-out-{idx}",
            "signal": signal,
            "source": "outset",
            "title": f"Study feedback: {_short(title, 90)}",
            "subtitle": f"{method} · {_short(summary, 120)}" if summary else str(method),
            "audience": item.get("audience") or "Shared",
            "theme": item.get("theme") or "Cross-audience",
            "product_area": item.get("product_area") or "Cross-platform",
            "date": item.get("created_at") or "",
            "severity": "MEDIUM",
            "evidence_snippet": summary[:240],
            "raw": item,
        })

    written = [
        c for c in cards
        if c["signal"] == SIGNAL_USER_FEEDBACK
        and (c["title"].startswith("User said:") or c["title"].startswith("User quote:"))
    ]
    study_fb = [
        c for c in cards
        if c["signal"] == SIGNAL_USER_FEEDBACK
        and (c["title"].startswith("Study feedback:") or c["title"].startswith("Research feedback:"))
    ]
    themed = [
        c for c in cards
        if c["signal"] == SIGNAL_USER_FEEDBACK
        and c not in written
        and c not in study_fb
    ]
    bugs = [c for c in cards if c["signal"] == SIGNAL_BUG]
    support = [c for c in cards if c["signal"] == SIGNAL_SUPPORT]
    friction = [c for c in cards if c["signal"] == SIGNAL_FRICTION]

    def by_date(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return sorted(rows, key=lambda c: str(c.get("date") or ""), reverse=True)

    ordered = (
        by_date(bugs)
        + by_date(written)
        + by_date(study_fb)
        + by_date(friction)
        + by_date(support)
        + by_date(themed)
    )

    # Cap per source so Affinity User reports shows Dovetail + Outset + Pendo
    caps = {"dovetail": 24, "outset": 12, "pendo": 16, "freshdesk": 8}
    capped: List[Dict[str, Any]] = []
    used = {k: 0 for k in caps}
    for c in ordered:
        src = c.get("source") or ""
        if src in caps and used[src] >= caps[src]:
            continue
        if src in used:
            used[src] += 1
        capped.append(c)
        if len(capped) >= limit:
            break
    return capped
