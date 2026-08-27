"""Classify research findings by audience (Brand / Partner) and UX theme."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# Explicit funnel → audience when name alone is ambiguous
FUNNEL_AUDIENCE: Dict[str, str] = {
    "Publisher/Partner Signup Flow": "Partner",
    "Onboarding Checklist": "Partner",
    "Login Flow": "Shared",
    "Contract Browse to Apply": "Partner",
    "UPS (Unified Proposal System) Flow": "Partner",
    "PublisherPro - Link Management": "Partner",
    "Finance/Reporting Access": "Partner",
    "Brand Finance Setup": "Brand",
    "Multi-Link Widget (MLW) Creation": "Partner",
    "Campaign Recruitment Flow": "Partner",
    "Brand Program Marketplace": "Brand",
    "Publisher Settings - Promotional Channels": "Partner",
    "Brand Storefronts Setup": "Brand",
}

# (theme, audience_hint, keywords) — first match wins; audience_hint None = infer from issue
THEME_RULES: List[Tuple[str, Optional[str], Tuple[str, ...]]] = [
    ("Signup & Onboarding", "Partner", ("signup", "onboarding", "checklist", "hang_tight", "account_details")),
    ("Login & Access", "Shared", ("login", "password", "email_screen", "authentication", "sign in")),
    ("Marketplace & Discovery", None, ("marketplace", "discover", "contract", "program_marketplace", "card_clicked", "browse")),
    ("Proposals & Campaigns", "Partner", ("ups", "proposal", "campaign", "recruitment", "instagram")),
    ("Finance & Payments", None, ("finance", "fincore", "billing", "balance", "payment", "invoice", "payout")),
    ("Link & Content Tools", "Partner", ("publisherpro", "ppx", "mlw", "microlink", "affiliate", "linkgen", "widget")),
    ("Settings & Profile", "Partner", ("settings", "promotional", "profile", "oauth", "connected_accounts", "channels")),
    ("Storefronts & Brand Setup", "Brand", ("storefront", "brand_finance", "brand setup", "storefronts")),
]

AUDIENCE_ORDER = ("Brand", "Partner", "Shared")
DEFAULT_TOP_ISSUES = 20


def rank_issues(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Rank by severity, drop-off rate, then user impact."""
    return sorted(
        issues,
        key=lambda x: (
            x.get("severity") != "HIGH",
            -float(x.get("drop_percentage") or 0),
            -int(x.get("users_affected") or 0),
        ),
    )


def select_top_issues(
    issues: List[Dict[str, Any]],
    limit: int = DEFAULT_TOP_ISSUES,
) -> List[Dict[str, Any]]:
    return rank_issues(issues)[:limit]


def _text_blob(issue: Dict[str, Any]) -> str:
    parts = [
        issue.get("funnel_name", ""),
        issue.get("title", ""),
        issue.get("step", ""),
    ]
    return " ".join(str(p) for p in parts).lower()


def classify_audience(issue: Dict[str, Any]) -> str:
    funnel = issue.get("funnel_name", "")
    if funnel in FUNNEL_AUDIENCE:
        return FUNNEL_AUDIENCE[funnel]

    blob = _text_blob(issue)
    brand_signals = ("brand:", "brand_", " brand ", "storefront")
    partner_signals = ("mediapartner", "publisher", "partner_", "ppx:", "publisherpro")

    is_brand = any(s in blob for s in brand_signals)
    is_partner = any(s in blob for s in partner_signals)

    if is_brand and not is_partner:
        return "Brand"
    if is_partner and not is_brand:
        return "Partner"
    if is_brand and is_partner:
        return "Shared"
    return "Shared"


def classify_theme(issue: Dict[str, Any]) -> str:
    blob = _text_blob(issue)
    audience = issue.get("audience") or classify_audience(issue)

    for theme, audience_hint, keywords in THEME_RULES:
        if any(kw in blob for kw in keywords):
            if audience_hint is None or audience_hint == audience or audience == "Shared":
                return theme

    if audience == "Brand":
        return "Brand Experience"
    if audience == "Partner":
        return "Partner Experience"
    return "Cross-audience"


def classify_research_item(item: Dict[str, Any]) -> Dict[str, str]:
    """Classify a Pendo/Freshdesk/Dovetail item for themed buckets."""
    pseudo = {
        "funnel_name": " ".join(
            filter(
                None,
                [
                    item.get("subject", ""),
                    item.get("title", ""),
                    item.get("guide_name", ""),
                    item.get("body", "")[:200],
                    item.get("response", "")[:200],
                    " ".join(item.get("tags") or []),
                ],
            )
        ),
        "title": item.get("subject") or item.get("title") or "",
        "step": "",
    }
    audience = classify_audience(pseudo)
    theme = classify_theme({**pseudo, "audience": audience})
    return {"audience": audience, "theme": theme}


def tag_issue(issue: Dict[str, Any]) -> Dict[str, Any]:
    tagged = dict(issue)
    tagged["audience"] = classify_audience(issue)
    tagged["theme"] = classify_theme(tagged)
    return tagged


def tag_issues(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [tag_issue(i) for i in issues]


def tag_research_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    tagged = []
    for item in items:
        copy = dict(item)
        meta = classify_research_item(item)
        copy.update(meta)
        tagged.append(copy)
    return tagged


def group_by_audience_and_theme(
    items: List[Dict[str, Any]],
    *,
    audience_key: str = "audience",
    theme_key: str = "theme",
) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    grouped: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
        audience: {} for audience in AUDIENCE_ORDER
    }

    for item in items:
        audience = item.get(audience_key, "Shared")
        theme = item.get(theme_key, "Other")
        if audience not in grouped:
            grouped[audience] = {}
        grouped[audience].setdefault(theme, []).append(item)

    # Sort issues within each theme by severity then users
    for audience in grouped:
        for theme in grouped[audience]:
            grouped[audience][theme].sort(
                key=lambda x: (
                    x.get("severity") != "HIGH",
                    -float(x.get("drop_percentage") or 0),
                    -int(x.get("users_affected") or 0),
                )
            )

    return grouped


def build_grouped_summary(grouped: Dict[str, Dict[str, List[Dict[str, Any]]]]) -> Dict[str, Any]:
    """Counts for report header stats."""
    summary: Dict[str, Any] = {}
    for audience in AUDIENCE_ORDER:
        themes = grouped.get(audience, {})
        issues = [i for theme_items in themes.values() for i in theme_items]
        summary[audience] = {
            "issue_count": len(issues),
            "high_severity": len([i for i in issues if i.get("severity") == "HIGH"]),
            "themes": {theme: len(items) for theme, items in themes.items()},
        }
    return summary
