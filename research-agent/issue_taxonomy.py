"""Classify research findings by audience, UX theme, and product area."""

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

FUNNEL_PRODUCT_AREA: Dict[str, str] = {
    "Publisher/Partner Signup Flow": "Signup & Onboarding",
    "Onboarding Checklist": "Signup & Onboarding",
    "Login Flow": "Login & Access",
    "Contract Browse to Apply": "Partner Discover",
    "UPS (Unified Proposal System) Flow": "Proposals & Campaigns",
    "PublisherPro - Link Management": "Partner Link Tools",
    "Finance/Reporting Access": "Partner Finance",
    "Brand Finance Setup": "Brand Finance",
    "Multi-Link Widget (MLW) Creation": "Partner Link Tools",
    "Campaign Recruitment Flow": "Proposals & Campaigns",
    "Brand Program Marketplace": "Brand Discover",
    "Publisher Settings - Promotional Channels": "Partner Settings",
    "Brand Storefronts Setup": "Brand Finance",
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

# (product_area, keywords) — first match wins; order matters
PRODUCT_AREA_RULES: List[Tuple[str, Tuple[str, ...]]] = [
    ("Brand Discover", ("brand - discover", "brand discover", "program marketplace", "find partners", "performance marketplace", "prospects")),
    ("Brand Engage", ("brand - engage", "brand engage", "creator premium", "engage:", "creator call", "creator deep dive", "stacked offers")),
    ("Brand Finance", ("brand - finance", "brand finance", "billing_group", "storefront")),
    ("Brand Protect", ("brand - protect", "brand protect", "forensiq")),
    ("Brand Optimize", ("brand - optimize", "brand optimize", "altitude")),
    ("Partner Discover", ("partner - discover", "partner discover", "find brands", "my brands", "brand marketplace", "discover_marketplace", "apply to brand", "contract browse")),
    ("Partner Home", ("partner - home", "partner home", "partner dashboard", "vnext partner")),
    ("Partner Content", ("partner - content", "partner content", "assets", "content:")),
    ("Partner Finance", ("partner - finance", "partner finance", "partner_balance", "fincore:partner", "finance/reporting")),
    ("Partner Settings", ("partner - settings", "publisher settings", "promotional channels", "connected_accounts")),
    ("Partner Link Tools", ("publisherpro", "ppx:", "mlw", "microlink", "linkgen", "affiliate link", "partner - brands")),
    ("Proposals & Campaigns", ("ups:", "proposal", "campaign recruitment", "unified proposal")),
    ("Signup & Onboarding", ("signup", "onboarding", "checklist", "hang_tight", "account_details", "brand direct signup")),
    ("Login & Access", ("login", "password_screen", "authentication", "sign in")),
    ("Messaging", ("messaging", "inbox", "notification")),
    ("Mobile", ("mobile app", "ios", "android")),
    ("Help Center", ("help center", "need help")),
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
        issue.get("guide_name", ""),
        issue.get("subject", ""),
        issue.get("subtitle", ""),
        issue.get("body", "")[:200] if isinstance(issue.get("body"), str) else "",
        issue.get("response", "")[:200] if isinstance(issue.get("response"), str) else "",
        issue.get("summary", "")[:200] if isinstance(issue.get("summary"), str) else "",
        issue.get("project_title", ""),
    ]
    return " ".join(str(p) for p in parts if p).lower()


def classify_audience(issue: Dict[str, Any]) -> str:
    funnel = issue.get("funnel_name", "")
    if funnel in FUNNEL_AUDIENCE:
        return FUNNEL_AUDIENCE[funnel]

    blob = _text_blob(issue)
    brand_signals = ("brand:", "brand -", "brand_", " brand ", "storefront", "advertiser")
    partner_signals = ("mediapartner", "publisher", "partner -", "partner_", "ppx:", "publisherpro")

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


def classify_product_area(issue: Dict[str, Any]) -> str:
    """Map a finding to a platform product area designers/PMs recognize."""
    funnel = issue.get("funnel_name", "")
    if funnel in FUNNEL_PRODUCT_AREA:
        return FUNNEL_PRODUCT_AREA[funnel]

    blob = _text_blob(issue)
    for area, keywords in PRODUCT_AREA_RULES:
        if any(kw in blob for kw in keywords):
            return area

    audience = issue.get("audience") or classify_audience(issue)
    if audience == "Brand":
        return "Brand General"
    if audience == "Partner":
        return "Partner General"
    return "Cross-platform"


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
                    item.get("subtitle", ""),
                    (item.get("body") or "")[:200],
                    (item.get("response") or "")[:200],
                    (item.get("summary") or "")[:200],
                    item.get("project_title", ""),
                    " ".join(item.get("tags") or []),
                ],
            )
        ),
        "title": item.get("subject") or item.get("title") or "",
        "step": "",
    }
    audience = classify_audience(pseudo)
    tagged = {**pseudo, "audience": audience}
    theme = classify_theme(tagged)
    product_area = classify_product_area({**tagged, "theme": theme})
    return {"audience": audience, "theme": theme, "product_area": product_area}


def tag_issue(issue: Dict[str, Any]) -> Dict[str, Any]:
    tagged = dict(issue)
    tagged["audience"] = classify_audience(issue)
    tagged["theme"] = classify_theme(tagged)
    tagged["product_area"] = classify_product_area(tagged)
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
