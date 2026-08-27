"""Fetch PostHog funnel drop-offs via the PostHog query API."""

from __future__ import annotations

import os
from typing import Any, Dict, List

import requests

from issue_taxonomy import rank_issues

POSTHOG_PROJECT_ID = os.environ.get("POSTHOG_PROJECT_ID", "186875")
POSTHOG_API_KEY = os.environ.get("POSTHOG_API_KEY", "")
POSTHOG_BASE_URL = os.environ.get("POSTHOG_BASE_URL", "https://us.posthog.com").rstrip("/")
DROP_OFF_THRESHOLD = float(os.environ.get("POSTHOG_DROP_OFF_THRESHOLD", "15"))

KEY_FUNNELS = [
    {
        "name": "Publisher/Partner Signup Flow",
        "events": [
            "SIGNUP:mediapartner_start_screen_view",
            "SIGNUP:mediapartner_email_screen_view",
            "SIGNUP:mediapartner_account_details_view",
            "SIGNUP:mediapartner_hang_tight_screen_view",
        ],
    },
    {
        "name": "Onboarding Checklist",
        "events": [
            "CHECKLIST:mediapartner_partner_profile_view",
            "CHECKLIST:mediapartner_business_model_view",
            "CHECKLIST:mediapartner_promotional_channels_view",
            "CHECKLIST:mediapartner_partner_profile_submit",
        ],
    },
    {
        "name": "Login Flow",
        "events": [
            "LOGIN:user_email_screen_view",
            "LOGIN:user_password_screen_view",
            "LOGIN:user_password_screen_submit",
        ],
    },
    {
        "name": "Contract Browse to Apply",
        "events": [
            "DISCOVER_MARKETPLACE:card_clicked",
            "DISCOVER_MARKETPLACE:proposal_sent",
        ],
    },
    {
        "name": "UPS (Unified Proposal System) Flow",
        "events": [
            "UPS:mediapartner_open",
            "UPS:mediapartner_tab_details_view",
            "UPS:mediapartner_modal_send_proposal_open",
            "UPS:mediapartner_modal_send_proposal_submit",
        ],
    },
    {
        "name": "PublisherPro - Link Management",
        "events": [
            "PPX:publisherpro_manage_links_load_microlink_destination",
            "PPX:publisherpro_manage_links_open_performance",
            "PPX:publisherpro_manage_links_open_linkgen_slideout",
            "PPX:publisherpro_affiliate_link_generated",
        ],
    },
    {
        "name": "Finance/Reporting Access",
        "events": [
            "FINCORE:shell_landing_page_view",
            "FINCORE:partner_balance_view",
            "FINCORE:partner_balance_transaction_list_load",
            "FINCORE:partner_finance_setup_view",
        ],
    },
    {
        "name": "Brand Finance Setup",
        "events": [
            "FINCORE:brand_finance_setup_view",
            "FINCORE:account_information_view",
            "FINCORE:billing_group_list_view",
            "FINCORE:billing_group_edit_view",
        ],
    },
    {
        "name": "Multi-Link Widget (MLW) Creation",
        "events": [
            "MLW:mediapartner_slideout_open",
            "MLW:mediapartner_task_selection_change",
            "MLW:mediapartner_link_create_api",
            "MLW:mediapartner_sync_impact_execute",
        ],
    },
    {
        "name": "Campaign Recruitment Flow",
        "events": [
            "UPS:mediapartner_modal_campaign_open",
            "UPS:mediapartner_learn_more_instagram_view",
            "UPS:mediapartner_modal_campaign_submit",
        ],
    },
    {
        "name": "Brand Program Marketplace",
        "events": [
            "BRAND:program_marketplace_search",
            "DISCOVER_MARKETPLACE:card_clicked",
            "DISCOVER_MARKETPLACE:proposal_sent",
        ],
    },
    {
        "name": "Publisher Settings - Promotional Channels",
        "events": [
            "PUBLISHER_SETTINGS:mediapartner_promotional_channels_view",
            "PUBLISHER_SETTINGS:mediapartner_promotional_channels_click",
            "PUBLISHER_SETTINGS:connected_accounts_oauth_callback",
            "PUBLISHER_SETTINGS:mediapartner_promotional_channels_submit",
        ],
    },
    {
        "name": "Brand Storefronts Setup",
        "events": [
            "FINCORE:shell_landing_page_view",
            "FINCORE:brand_finance_setup_view",
            "CHECKLIST:mediapartner_partner_profile_view",
            "FINCORE:settings_save",
        ],
    },
]


def _query_funnels(lookback_days: int) -> List[Dict[str, Any]]:
    if not POSTHOG_API_KEY:
        print("  ⚠️  PostHog API key not set, skipping")
        return []

    funnels_data: List[Dict[str, Any]] = []
    url = f"{POSTHOG_BASE_URL}/api/projects/{POSTHOG_PROJECT_ID}/query/"
    headers = {
        "Authorization": f"Bearer {POSTHOG_API_KEY}",
        "Content-Type": "application/json",
    }

    for funnel in KEY_FUNNELS:
        try:
            series = [{"kind": "EventsNode", "event": event} for event in funnel["events"]]
            payload = {
                "query": {
                    "kind": "FunnelsQuery",
                    "series": series,
                    "dateRange": {"date_from": f"-{lookback_days}d"},
                    "filterTestAccounts": True,
                }
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            if isinstance(results, list) and len(results) >= 2:
                funnels_data.append({
                    "funnel_name": funnel["name"],
                    "events": funnel["events"],
                    "data": {"data": results},
                })
                print(f"  ✅ {funnel['name']}")
        except Exception as exc:
            print(f"  ⚠️  {funnel['name']}: {exc}")

    return funnels_data


def _analyze_funnels(funnel_results: List[Dict[str, Any]], threshold: float) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []

    for funnel in funnel_results:
        funnel_name = funnel["funnel_name"]
        data = funnel.get("data", {})
        if "data" not in data:
            continue

        steps = data.get("data", [])
        for i in range(1, len(steps)):
            prev_step = steps[i - 1]
            curr_step = steps[i]
            prev_count = prev_step.get("count", 0)
            curr_count = curr_step.get("count", 0)

            if prev_count <= 0:
                continue

            drop_percentage = ((prev_count - curr_count) / prev_count) * 100
            if drop_percentage <= threshold:
                continue

            issues.append({
                "source": "posthog",
                "title": f"{funnel_name} - Step {i} Drop-off",
                "funnel_name": funnel_name,
                "severity": "HIGH" if drop_percentage > 30 else "MEDIUM",
                "drop_percentage": round(drop_percentage, 2),
                "users_affected": curr_count,
                "step": f"{funnel['events'][i - 1]} → {funnel['events'][i]}",
                "metrics": {
                    "step_from": prev_count,
                    "step_to": curr_count,
                    "drop_percentage": round(drop_percentage, 2),
                },
                "posthog_link": f"{POSTHOG_BASE_URL}/project/{POSTHOG_PROJECT_ID}/insights",
            })

    return rank_issues(issues)


def query_posthog_dropoffs(
    lookback_days: int = 90,
    threshold: float = DROP_OFF_THRESHOLD,
) -> List[Dict[str, Any]]:
    """Query all monitored funnels and return every significant drop-off in the period."""
    print("\n🔍 Querying PostHog funnels...")
    funnel_results = _query_funnels(lookback_days)
    print(
        f"\n📊 Analyzing {len(funnel_results)} funnels for drop-offs > {threshold}%..."
    )
    issues = _analyze_funnels(funnel_results, threshold)
    print(f"  Found {len(issues)} significant drop-offs (last {lookback_days} days)")
    return issues
