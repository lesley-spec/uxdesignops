#!/usr/bin/env python3
"""
Research Insight Monitor Agent - Cloud Edition
Runs in GitHub Actions, saves findings to Confluence
"""

import os
import sys
from pathlib import Path

# Load .env before other modules read os.environ
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

import json
import requests
from datetime import datetime, timedelta
from typing import Optional, List, Dict

from freshdesk_bigquery import query_freshdesk_tickets
from report_publisher import build_report_payload, publish_github_pages_report

# Configuration from environment variables
POSTHOG_PROJECT_ID = os.environ.get("POSTHOG_PROJECT_ID", "186875")
POSTHOG_API_KEY = os.environ.get("POSTHOG_API_KEY", "")
POSTHOG_BASE_URL = "https://us.posthog.com"

PENDO_API_KEY = os.environ.get("PENDO_API_KEY", "")
PENDO_SUBSCRIPTION_ID = os.environ.get("PENDO_SUBSCRIPTION_ID", "")
PENDO_REGION = os.environ.get("PENDO_REGION", "US").upper()

OUTSET_API_KEY = os.environ.get("OUTSET_API_KEY", "")
DOVETAIL_API_KEY = os.environ.get("DOVETAIL_API_KEY", "") or os.environ.get("DOVETAIL_API_TOKEN", "")
DOVETAIL_BASE_URL = os.environ.get("DOVETAIL_BASE_URL", "https://dovetail.com")

PENDO_REGION_URLS = {
    "US": "https://app.pendo.io",
    "EU": "https://app.eu.pendo.io",
    "US1": "https://us1.app.pendo.io",
    "JPN": "https://app.jpn.pendo.io",
    "AU": "https://app.au.pendo.io",
}

RESEARCH_STOPWORDS = {
    "flow", "the", "and", "for", "with", "from", "step", "drop", "off", "to", "a", "an"
}

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
SYNTHESIS_MODEL = os.environ.get("SYNTHESIS_MODEL", "google")

CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL", "")
CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME", "")
CONFLUENCE_API_TOKEN = os.environ.get("CONFLUENCE_API_TOKEN", "")
CONFLUENCE_SPACE = os.environ.get("CONFLUENCE_SPACE", "ux")

PUBLISH_CONFLUENCE = os.environ.get("PUBLISH_CONFLUENCE", "true").lower() not in {"0", "false", "no"}
PUBLISH_GITHUB_PAGES = os.environ.get("PUBLISH_GITHUB_PAGES", "true").lower() not in {"0", "false", "no"}
GITHUB_PAGES_URL = os.environ.get("GITHUB_PAGES_URL", "")

DROP_OFF_THRESHOLD = 15

# Define all 13 funnels
KEY_FUNNELS = [
    {"name": "Publisher/Partner Signup Flow", "events": [
        "SIGNUP:mediapartner_start_screen_view",
        "SIGNUP:mediapartner_email_screen_view",
        "SIGNUP:mediapartner_account_details_view",
        "SIGNUP:mediapartner_hang_tight_screen_view"
    ]},
    {"name": "Onboarding Checklist", "events": [
        "CHECKLIST:mediapartner_partner_profile_view",
        "CHECKLIST:mediapartner_business_model_view",
        "CHECKLIST:mediapartner_promotional_channels_view",
        "CHECKLIST:mediapartner_partner_profile_submit"
    ]},
    {"name": "Login Flow", "events": [
        "LOGIN:user_email_screen_view",
        "LOGIN:user_password_screen_view",
        "LOGIN:user_password_screen_submit"
    ]},
    {"name": "Contract Browse to Apply", "events": [
        "DISCOVER_MARKETPLACE:card_clicked",
        "DISCOVER_MARKETPLACE:proposal_sent"
    ]},
    {"name": "UPS (Unified Proposal System) Flow", "events": [
        "UPS:mediapartner_open",
        "UPS:mediapartner_tab_details_view",
        "UPS:mediapartner_modal_send_proposal_open",
        "UPS:mediapartner_modal_send_proposal_submit"
    ]},
    {"name": "PublisherPro - Link Management", "events": [
        "PPX:publisherpro_manage_links_load_microlink_destination",
        "PPX:publisherpro_manage_links_open_performance",
        "PPX:publisherpro_manage_links_open_linkgen_slideout",
        "PPX:publisherpro_affiliate_link_generated"
    ]},
    {"name": "Finance/Reporting Access", "events": [
        "FINCORE:shell_landing_page_view",
        "FINCORE:partner_balance_view",
        "FINCORE:partner_balance_transaction_list_load",
        "FINCORE:partner_finance_setup_view"
    ]},
    {"name": "Brand Finance Setup", "events": [
        "FINCORE:brand_finance_setup_view",
        "FINCORE:account_information_view",
        "FINCORE:billing_group_list_view",
        "FINCORE:billing_group_edit_view"
    ]},
    {"name": "Multi-Link Widget (MLW) Creation", "events": [
        "MLW:mediapartner_slideout_open",
        "MLW:mediapartner_task_selection_change",
        "MLW:mediapartner_link_create_api",
        "MLW:mediapartner_sync_impact_execute"
    ]},
    {"name": "Campaign Recruitment Flow", "events": [
        "UPS:mediapartner_modal_campaign_open",
        "UPS:mediapartner_learn_more_instagram_view",
        "UPS:mediapartner_modal_campaign_submit"
    ]},
    {"name": "Brand Program Marketplace", "events": [
        "BRAND:program_marketplace_search",
        "DISCOVER_MARKETPLACE:card_clicked",
        "DISCOVER_MARKETPLACE:proposal_sent"
    ]},
    {"name": "Publisher Settings - Promotional Channels", "events": [
        "PUBLISHER_SETTINGS:mediapartner_promotional_channels_view",
        "PUBLISHER_SETTINGS:mediapartner_promotional_channels_click",
        "PUBLISHER_SETTINGS:connected_accounts_oauth_callback",
        "PUBLISHER_SETTINGS:mediapartner_promotional_channels_submit"
    ]},
    {"name": "Brand Storefronts Setup", "events": [
        "FINCORE:shell_landing_page_view",
        "FINCORE:brand_finance_setup_view",
        "CHECKLIST:mediapartner_partner_profile_view",
        "FINCORE:settings_save"
    ]}
]


def get_pendo_base_url() -> str:
    """Resolve Pendo API base URL from region or integration key suffix."""
    if PENDO_REGION in PENDO_REGION_URLS:
        return PENDO_REGION_URLS[PENDO_REGION]

    if PENDO_API_KEY and "." in PENDO_API_KEY:
        suffix = PENDO_API_KEY.rsplit(".", 1)[-1].lower()
        region_map = {"us": "US", "eu": "EU", "us1": "US1", "jpn": "JPN", "au": "AU"}
        region = region_map.get(suffix)
        if region:
            return PENDO_REGION_URLS[region]

    return PENDO_REGION_URLS["US"]


def extract_search_terms(text: str) -> List[str]:
    """Extract meaningful keywords for matching research evidence to issues."""
    tokens = []
    for part in text.replace("/", " ").replace("-", " ").replace("_", " ").split():
        word = part.strip().lower()
        if len(word) >= 3 and word not in RESEARCH_STOPWORDS:
            tokens.append(word)
    return tokens


class ResearchInsightAgentCloud:
    """Cloud-based research insight agent"""

    def __init__(self):
        self.issues = []
        self.week_start = self.get_week_start()
        self.report_date = datetime.utcnow().strftime("%Y-%m-%d")

    @staticmethod
    def get_week_start():
        """Get Monday of current week"""
        today = datetime.utcnow()
        monday = today - timedelta(days=today.weekday())
        return monday.strftime("%Y-%m-%d")

    def query_posthog_funnels(self) -> List[Dict]:
        """Query PostHog for funnel data"""
        print("\n🔍 Querying PostHog funnels...")

        if not POSTHOG_API_KEY:
            print("  ⚠️  PostHog API key not set, skipping")
            return []

        funnels_data = []

        for funnel in KEY_FUNNELS:
            try:
                url = f"{POSTHOG_BASE_URL}/api/projects/{POSTHOG_PROJECT_ID}/query/"
                series = [{"kind": "EventsNode", "event": event} for event in funnel["events"]]
                payload = {
                    "kind": "FunnelsQuery",
                    "series": series,
                    "dateRange": {"date_from": "-7d"},
                    "filterTestAccounts": True
                }
                headers = {
                    "Authorization": f"Bearer {POSTHOG_API_KEY}",
                    "Content-Type": "application/json"
                }

                response = requests.post(url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()

                data = response.json()
                if "results" in data and isinstance(data["results"], list) and len(data["results"]) > 0:
                    funnels_data.append({
                        "funnel_name": funnel["name"],
                        "events": funnel["events"],
                        "data": data["results"][0]
                    })
                    print(f"  ✅ {funnel['name']}")

            except Exception as e:
                print(f"  ⚠️  {funnel['name']}: {str(e)}")

        return funnels_data

    def analyze_funnels(self, funnel_results: List[Dict]) -> List[Dict]:
        """Analyze funnels for drop-offs"""
        print(f"\n📊 Analyzing {len(funnel_results)} funnels for drop-offs > {DROP_OFF_THRESHOLD}%...")

        issues = []

        for funnel in funnel_results:
            funnel_name = funnel["funnel_name"]
            data = funnel.get("data", {})

            if "data" not in data:
                continue

            steps = data.get("data", [])

            for i in range(1, len(steps)):
                prev_step = steps[i-1]
                curr_step = steps[i]

                prev_count = prev_step.get("count", 0)
                curr_count = curr_step.get("count", 0)

                if prev_count > 0:
                    drop_percentage = ((prev_count - curr_count) / prev_count) * 100

                    if drop_percentage > DROP_OFF_THRESHOLD:
                        issues.append({
                            "title": f"{funnel_name} - Step {i} Drop-off",
                            "funnel_name": funnel_name,
                            "severity": "HIGH" if drop_percentage > 30 else "MEDIUM",
                            "drop_percentage": round(drop_percentage, 2),
                            "users_affected": curr_count,
                            "step": f"{funnel['events'][i-1]} → {funnel['events'][i]}",
                            "metrics": {
                                "step_from": prev_count,
                                "step_to": curr_count,
                                "drop_percentage": round(drop_percentage, 2)
                            },
                            "posthog_link": f"{POSTHOG_BASE_URL}/project/{POSTHOG_PROJECT_ID}/insights"
                        })

        # Sort by severity then user impact
        issues = sorted(issues, key=lambda x: (x['severity'] != 'HIGH', -x['users_affected']))

        print(f"  Found {len(issues)} significant drop-offs")
        return issues

    def _pendo_aggregate(self, pipeline: List[Dict], request_id: str) -> List[Dict]:
        """Run a Pendo Aggregation API query."""
        base_url = get_pendo_base_url()
        url = f"{base_url}/api/v1/aggregation"
        headers = {
            "Content-Type": "application/json",
            "X-Pendo-Integration-Key": PENDO_API_KEY,
        }
        payload = {
            "response": {"mimeType": "application/json"},
            "request": {"requestId": request_id, "pipeline": pipeline},
        }

        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            results = data.get("results")
            if isinstance(results, list):
                return results
            if results is not None:
                return [results]
        return []

    def query_pendo_feedback(self) -> List[Dict]:
        """Fetch recent open-text poll responses from Pendo."""
        print("\n💬 Querying Pendo in-app feedback...")

        if not PENDO_API_KEY:
            print("  ⚠️  Pendo API key not set, skipping")
            return []

        feedback = []

        try:
            guides = self._pendo_aggregate([{"source": {"guides": None}}], "research-agent-guides")
            guide_names = {
                guide.get("id"): guide.get("name", "Unknown guide")
                for guide in guides
                if guide.get("id")
            }

            poll_events = self._pendo_aggregate(
                [{
                    "source": {
                        "pollEvents": None,
                        "timeSeries": {
                            "period": "dayRange",
                            "first": 'date_add(now(), -7, "days")',
                            "count": 7,
                        },
                    }
                }],
                "research-agent-poll-events",
            )

            for event in poll_events:
                response_text = event.get("pollResponse")
                if not isinstance(response_text, str) or not response_text.strip():
                    continue

                guide_id = event.get("guideId", "")
                feedback.append({
                    "source": "pendo",
                    "guide_id": guide_id,
                    "guide_name": guide_names.get(guide_id, guide_id or "Unknown guide"),
                    "poll_id": event.get("pollId", ""),
                    "response": response_text.strip(),
                    "visitor_id": event.get("visitorId", ""),
                    "timestamp": event.get("browserTime") or event.get("time"),
                    "search_terms": extract_search_terms(
                        f"{guide_names.get(guide_id, '')} {response_text}"
                    ),
                })

            print(f"  ✅ Found {len(feedback)} open-text poll responses")

        except Exception as e:
            print(f"  ⚠️  Pendo query failed: {str(e)}")

        return feedback

    def query_dovetail_insights(self, issues: List[Dict]) -> List[Dict]:
        """Search Dovetail for insights and highlights related to detected issues."""
        print("\n📚 Querying Dovetail research insights...")

        if not DOVETAIL_API_KEY:
            print("  ⚠️  Dovetail API key not set, skipping")
            return []

        if not issues:
            print("  ⚠️  No issues to search against, skipping")
            return []

        insights = []
        seen_ids = set()
        search_queries = set()

        for issue in issues[:8]:
            terms = extract_search_terms(issue["funnel_name"])
            if terms:
                search_queries.add(" ".join(terms[:4]))

        if not search_queries:
            search_queries.add("ux onboarding signup")

        headers = {
            "Authorization": f"Bearer {DOVETAIL_API_KEY}",
            "Content-Type": "application/json",
        }
        url = f"{DOVETAIL_BASE_URL}/api/v2/search"

        for query in search_queries:
            try:
                payload = {
                    "offset": 0,
                    "limit": 10,
                    "options": {
                        "query": query,
                        "types": ["INSIGHT", "HIGHLIGHT", "NOTE"],
                        "archived": False,
                    },
                }

                response = requests.post(url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()
                data = response.json()

                for result_type in ("insights", "highlights", "notes"):
                    for item in data.get(result_type, []):
                        item_id = item.get("id")
                        if not item_id or item_id in seen_ids:
                            continue

                        seen_ids.add(item_id)
                        title = item.get("title", "Untitled")
                        preview = item.get("preview_text") or item.get("content") or ""
                        if isinstance(preview, dict):
                            preview = preview.get("text", "")

                        insights.append({
                            "source": "dovetail",
                            "type": result_type.rstrip("s"),
                            "id": item_id,
                            "title": title,
                            "preview": str(preview)[:500],
                            "url": item.get("url", ""),
                            "project_title": item.get("project_title", ""),
                            "search_terms": extract_search_terms(f"{title} {preview}"),
                            "query": query,
                        })

            except Exception as e:
                print(f"  ⚠️  Dovetail search for '{query}': {str(e)}")

        print(f"  ✅ Found {len(insights)} Dovetail research items")
        return insights

    def query_outset_studies(self) -> List[Dict]:
        """Outset has no public REST API — MCP/OAuth only."""
        print("\n🎙️  Querying Outset studies...")

        if OUTSET_API_KEY:
            print("  ⚠️  Outset REST API is not publicly available yet")
            print("  ℹ️  Use Outset MCP in Cursor for interactive study access")
        else:
            print("  ⚠️  Outset not configured (REST API unavailable; use MCP in Cursor)")

        return []

    def query_freshdesk_support_tickets(self) -> List[Dict]:
        """Fetch recent support tickets from Freshworks via BigQuery."""
        return query_freshdesk_tickets()

    def enrich_issues_with_research(
        self,
        issues: List[Dict],
        pendo_feedback: List[Dict],
        dovetail_insights: List[Dict],
        freshdesk_tickets: List[Dict],
        outset_studies: List[Dict],
    ) -> List[Dict]:
        """Attach qualitative research evidence to quantitative funnel issues."""
        print("\n🔗 Enriching issues with research evidence...")

        for issue in issues:
            issue_terms = set(extract_search_terms(issue["funnel_name"]))
            issue_terms.update(extract_search_terms(issue.get("step", "")))

            matched_pendo = []
            matched_dovetail = []
            matched_freshdesk = []
            matched_outset = []

            for item in pendo_feedback:
                item_terms = set(item.get("search_terms", []))
                if issue_terms & item_terms:
                    matched_pendo.append(item)

            for item in dovetail_insights:
                item_terms = set(item.get("search_terms", []))
                if issue_terms & item_terms:
                    matched_dovetail.append(item)

            for item in freshdesk_tickets:
                item_terms = set(item.get("search_terms", []))
                if issue_terms & item_terms:
                    matched_freshdesk.append(item)

            for item in outset_studies:
                item_terms = set(item.get("search_terms", []))
                if issue_terms & item_terms:
                    matched_outset.append(item)

            source_count = sum([
                bool(matched_pendo),
                bool(matched_dovetail),
                bool(matched_freshdesk),
            ])

            issue["research_context"] = {
                "pendo_feedback": matched_pendo[:3],
                "dovetail_insights": matched_dovetail[:3],
                "freshdesk_tickets": matched_freshdesk[:3],
                "outset_studies": matched_outset[:3],
                "triangulated": source_count >= 2,
            }

        enriched_count = len([
            i for i in issues
            if i["research_context"]["pendo_feedback"]
            or i["research_context"]["dovetail_insights"]
            or i["research_context"]["freshdesk_tickets"]
            or i["research_context"]["outset_studies"]
        ])
        print(f"  ✅ Enriched {enriched_count}/{len(issues)} issues with research context")
        return issues

    @staticmethod
    def format_research_context(context: Dict) -> str:
        """Format research evidence for prompts and Confluence pages."""
        sections = []

        for item in context.get("pendo_feedback", []):
            sections.append(
                f"Pendo ({item.get('guide_name', 'Guide')}): \"{item.get('response', '')}\""
            )

        for item in context.get("dovetail_insights", []):
            preview = item.get("preview", "")
            sections.append(
                f"Dovetail {item.get('type', 'insight')} — {item.get('title', 'Untitled')}: {preview[:200]}"
            )

        for item in context.get("freshdesk_tickets", []):
            sections.append(
                f"Freshdesk ({item.get('ticket_type', 'ticket')}) — {item.get('subject', 'Untitled')}: "
                f"{item.get('body', '')[:200]}"
            )

        for item in context.get("outset_studies", []):
            sections.append(
                f"Outset study — {item.get('title', 'Untitled')}: {item.get('summary', '')[:200]}"
            )

        return "\n".join(sections) if sections else "No related qualitative research found."

    def synthesize_with_gemini(self, issues: List[Dict]) -> Dict[str, str]:
        """Synthesize findings with Google Gemini"""
        if not issues:
            return {}

        print(f"\n🧠 Synthesizing {len(issues)} findings with Google Gemini...")

        if not GOOGLE_API_KEY:
            print("  ⚠️  Google API key not set, using mock synthesis")
            return self.mock_synthesis(issues)

        synthesis = {}

        for issue in issues[:5]:  # Synthesize top 5 only
            try:
                research_context = self.format_research_context(
                    issue.get("research_context", {})
                )
                prompt = f"""You are a UX analyst. Analyze this funnel drop-off and provide:
1. What's happening (why users drop off)
2. Why it matters (user impact)
3. What to investigate next

Funnel: {issue['funnel_name']}
Drop-off: {issue['drop_percentage']}% at step {issue['title'].split('-')[-1]}
Users Affected: {issue['users_affected']}

Related qualitative research:
{research_context}

Provide a concise 2-3 sentence analysis that connects the quantitative drop-off with any relevant research evidence."""

                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }
                params = {"key": GOOGLE_API_KEY}

                response = requests.post(url, json=payload, headers=headers, params=params, timeout=30)
                response.raise_for_status()

                data = response.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    synthesis[issue["title"]] = text
                    print(f"  ✅ {issue['funnel_name']}")

            except Exception as e:
                print(f"  ⚠️  Synthesis error for {issue['funnel_name']}: {str(e)}")
                synthesis[issue["title"]] = f"Drop-off detected: {issue['drop_percentage']}% of users affected"

        return synthesis

    def mock_synthesis(self, issues: List[Dict]) -> Dict[str, str]:
        """Fallback synthesis without API"""
        synthesis = {}
        for issue in issues[:5]:
            synthesis[issue["title"]] = f"{issue['drop_percentage']}% drop-off detected. {issue['users_affected']} users affected."
        return synthesis

    def _confluence_find_page(self, title: str) -> Optional[Dict]:
        """Find an existing Confluence page by title in the configured space."""
        auth = (CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN)
        url = f"{CONFLUENCE_URL}/rest/api/content"
        params = {"title": title, "spaceKey": CONFLUENCE_SPACE, "expand": "version"}
        response = requests.get(url, params=params, auth=auth, timeout=30)
        response.raise_for_status()
        results = response.json().get("results", [])
        return results[0] if results else None

    def _confluence_upsert_page(self, title: str, html_content: str, labels: List[str]) -> Optional[str]:
        """Create or update a Confluence page and return its URL."""
        auth = (CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN)
        existing = self._confluence_find_page(title)

        payload = {
            "type": "page",
            "title": title,
            "space": {"key": CONFLUENCE_SPACE},
            "body": {
                "storage": {
                    "value": html_content,
                    "representation": "storage",
                }
            },
            "metadata": {
                "labels": [{"name": label} for label in labels],
            },
        }

        if existing:
            page_id = existing["id"]
            payload["id"] = page_id
            payload["version"] = {"number": existing["version"]["number"] + 1}
            url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}"
            response = requests.put(url, json=payload, auth=auth, timeout=30)
        else:
            url = f"{CONFLUENCE_URL}/rest/api/content"
            response = requests.post(url, json=payload, auth=auth, timeout=30)

        response.raise_for_status()
        page_data = response.json()
        return f"{CONFLUENCE_URL}/pages/viewpage.action?pageId={page_data['id']}"

    def create_confluence_weekly_report(
        self,
        issues: List[Dict],
        synthesis: Dict[str, str],
        pendo_feedback: List[Dict],
        dovetail_insights: List[Dict],
        freshdesk_tickets: List[Dict],
        github_report_url: Optional[str] = None,
    ) -> Optional[str]:
        """Create or update weekly report page in Confluence"""
        if not PUBLISH_CONFLUENCE:
            print("  ℹ️  Confluence publishing disabled (PUBLISH_CONFLUENCE=false)")
            return None

        if not CONFLUENCE_URL or not CONFLUENCE_API_TOKEN:
            print("  ⚠️  Confluence credentials not set")
            return None

        print(f"\n📝 Creating weekly report in Confluence...")

        try:
            high_severity = len([i for i in issues if i['severity'] == 'HIGH'])
            medium_severity = len([i for i in issues if i['severity'] == 'MEDIUM'])
            triangulated = len([i for i in issues if i.get("research_context", {}).get("triangulated")])

            top_5_html = ""
            for issue in issues[:5]:
                analysis = synthesis.get(issue["title"], "Analysis pending.")
                tri = " ✅ Triangulated" if issue.get("research_context", {}).get("triangulated") else ""
                top_5_html += f"""
                <li>
                    <strong>{issue['title']}</strong>{tri}<br/>
                    <em>Drop: {issue['drop_percentage']}% | Users: {issue['users_affected']}</em><br/>
                    Severity: <strong>{issue['severity']}</strong><br/>
                    <p>{analysis}</p>
                </li>
                """

            github_link_html = (
                f'<p><strong>Web report:</strong> <a href="{github_report_url}">{github_report_url}</a></p>'
                if github_report_url else ""
            )

            html_content = f"""
            <h1>📊 Weekly Research Report: Week of {self.week_start}</h1>
            {github_link_html}

            <h2>Executive Summary</h2>
            <p><strong>{len(issues)}</strong> UX issues identified this week:</p>
            <ul>
                <li><strong>{high_severity}</strong> High-severity issues</li>
                <li><strong>{medium_severity}</strong> Medium-severity issues</li>
                <li><strong>{triangulated}</strong> Triangulated (2+ research sources)</li>
            </ul>

            <h2>Top Issues</h2>
            <ol>
                {top_5_html}
            </ol>

            <h2>All Issues</h2>
            <table>
                <thead>
                    <tr>
                        <th>Issue</th>
                        <th>Severity</th>
                        <th>Drop %</th>
                        <th>Users Affected</th>
                        <th>Triangulated</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join([f"<tr><td>{i['title']}</td><td>{i['severity']}</td><td>{i['drop_percentage']}%</td><td>{i['users_affected']}</td><td>{'Yes' if i.get('research_context', {}).get('triangulated') else 'No'}</td></tr>" for i in issues])}
                </tbody>
            </table>

            <h2>Research Sources This Week</h2>
            <ul>
                <li><strong>Pendo feedback:</strong> {len(pendo_feedback)} open-text poll responses</li>
                <li><strong>Dovetail insights:</strong> {len(dovetail_insights)} related research items</li>
                <li><strong>Freshdesk tickets:</strong> {len(freshdesk_tickets)} support tickets (BigQuery)</li>
            </ul>

            <hr/>
            <p><em>Generated: {datetime.utcnow().isoformat()}</em></p>
            """

            page_url = self._confluence_upsert_page(
                title=f"Weekly Report: Week of {self.week_start}",
                html_content=html_content,
                labels=["research", "weekly-report"],
            )
            print(f"  ✅ Weekly report saved: {page_url}")
            return page_url

        except Exception as e:
            print(f"  ❌ Failed to create weekly report: {str(e)}")
            return None

    def create_confluence_issue_pages(self, issues: List[Dict], synthesis: Dict[str, str]) -> List[str]:
        """Create or update individual issue pages in Confluence"""
        if not PUBLISH_CONFLUENCE:
            return []

        if not CONFLUENCE_URL or not CONFLUENCE_API_TOKEN:
            return []

        print(f"\n📄 Creating issue pages in Confluence...")

        page_urls = []

        for issue in issues[:10]:
            try:
                severity_color = "#d32f2f" if issue['severity'] == 'HIGH' else "#f57c00"
                issue_synthesis = synthesis.get(issue['title'], 'Analysis pending.')
                research_context = issue.get("research_context", {})
                research_html = ""

                for item in research_context.get("pendo_feedback", []):
                    research_html += f"<li><strong>Pendo</strong> ({item.get('guide_name', 'Guide')}): \"{item.get('response', '')}\"</li>"

                for item in research_context.get("dovetail_insights", []):
                    link = item.get("url", "")
                    title = item.get("title", "Untitled")
                    if link:
                        research_html += f"<li><strong>Dovetail</strong>: <a href=\"{link}\">{title}</a></li>"
                    else:
                        research_html += f"<li><strong>Dovetail</strong>: {title}</li>"

                for item in research_context.get("freshdesk_tickets", []):
                    link = item.get("url", "")
                    subject = item.get("subject", "Support ticket")
                    if link:
                        research_html += f"<li><strong>Freshdesk</strong>: <a href=\"{link}\">{subject}</a></li>"
                    else:
                        research_html += f"<li><strong>Freshdesk</strong>: {subject}</li>"

                if not research_html:
                    research_html = "<li>No related qualitative research found.</li>"

                triangulated = "Yes — 2+ independent sources agree" if research_context.get("triangulated") else "No"

                html_content = f"""
                <h1 style="color: {severity_color}">🔍 {issue['title']}</h1>

                <h2>Metrics</h2>
                <table>
                    <tr><td><strong>Severity</strong></td><td>{issue['severity']}</td></tr>
                    <tr><td><strong>Drop-off %</strong></td><td>{issue['drop_percentage']}%</td></tr>
                    <tr><td><strong>Users Affected</strong></td><td>{issue['users_affected']}</td></tr>
                    <tr><td><strong>Funnel</strong></td><td>{issue['funnel_name']}</td></tr>
                    <tr><td><strong>Step</strong></td><td>{issue['step']}</td></tr>
                    <tr><td><strong>Triangulated</strong></td><td>{triangulated}</td></tr>
                </table>

                <h2>Analysis</h2>
                <p>{issue_synthesis}</p>

                <h2>Related Research</h2>
                <ul>
                    {research_html}
                </ul>

                <h2>Details</h2>
                <ul>
                    <li>Users entering step: {issue['metrics']['step_from']}</li>
                    <li>Users completing step: {issue['metrics']['step_to']}</li>
                    <li>Drop-off calculation: ({issue['metrics']['step_from']} - {issue['metrics']['step_to']}) / {issue['metrics']['step_from']} = {issue['drop_percentage']}%</li>
                </ul>

                <h2>Links</h2>
                <ul>
                    <li><a href="{issue['posthog_link']}">View in PostHog</a></li>
                </ul>

                <hr/>
                <p><em>Generated: {datetime.utcnow().isoformat()}</em></p>
                """

                tags = ["research", issue['severity'].lower()]
                if "contract" in issue['funnel_name'].lower():
                    tags.append("contracts")
                if "publisher" in issue['funnel_name'].lower() or "signup" in issue['funnel_name'].lower():
                    tags.append("publisher")
                if "brand" in issue['funnel_name'].lower():
                    tags.append("brand")

                page_url = self._confluence_upsert_page(
                    title=issue['title'],
                    html_content=html_content,
                    labels=tags,
                )
                page_urls.append(page_url)
                print(f"  ✅ {issue['title']}")

            except Exception as e:
                print(f"  ⚠️  Failed to create page for {issue['title']}: {str(e)}")

        return page_urls

    def run(self) -> Dict:
        """Execute full agent pipeline"""
        print("="*70)
        print("🚀 Research Insight Monitor Agent (Cloud Edition)")
        print("="*70)
        print(f"   Time: {datetime.utcnow().isoformat()}")
        print(f"   Week: {self.week_start}")

        # Step 1: Query PostHog
        funnel_results = self.query_posthog_funnels()

        # Step 2: Analyze for drop-offs
        self.issues = self.analyze_funnels(funnel_results)

        # Step 3: Gather qualitative research from other sources
        pendo_feedback = self.query_pendo_feedback()
        dovetail_insights = self.query_dovetail_insights(self.issues)
        freshdesk_tickets = self.query_freshdesk_support_tickets()
        outset_studies = self.query_outset_studies()

        # Step 4: Enrich issues with research context
        self.issues = self.enrich_issues_with_research(
            self.issues, pendo_feedback, dovetail_insights, freshdesk_tickets, outset_studies
        )

        # Step 5: Synthesize with Gemini
        synthesis = self.synthesize_with_gemini(self.issues)

        # Step 6: Publish linkable report (GitHub Pages)
        github_report_url = None
        if PUBLISH_GITHUB_PAGES:
            print("\n🌐 Publishing GitHub Pages report...")
            payload = build_report_payload(
                week_start=self.week_start,
                issues=self.issues,
                synthesis=synthesis,
                pendo_feedback=pendo_feedback,
                dovetail_insights=dovetail_insights,
                freshdesk_tickets=freshdesk_tickets,
                outset_studies=outset_studies,
            )
            github_report_url = publish_github_pages_report(payload)

        # Step 7: Save to Confluence (optional)
        print("\n📤 Saving to Confluence...")
        weekly_report_url = self.create_confluence_weekly_report(
            self.issues,
            synthesis,
            pendo_feedback,
            dovetail_insights,
            freshdesk_tickets,
            github_report_url=github_report_url,
        )
        issue_pages = self.create_confluence_issue_pages(self.issues, synthesis)

        if github_report_url and weekly_report_url is None:
            print(f"\n🔗 Share this report: {github_report_url}")

        print("\n" + "="*70)
        print("✨ Agent run complete!")
        print("="*70)

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "week": self.week_start,
            "issues_found": len(self.issues),
            "high_severity": len([i for i in self.issues if i['severity'] == 'HIGH']),
            "medium_severity": len([i for i in self.issues if i['severity'] == 'MEDIUM']),
            "pendo_feedback_count": len(pendo_feedback),
            "dovetail_insights_count": len(dovetail_insights),
            "freshdesk_tickets_count": len(freshdesk_tickets),
            "outset_studies_count": len(outset_studies),
            "issues_with_research_context": len([
                i for i in self.issues
                if i.get("research_context", {}).get("pendo_feedback")
                or i.get("research_context", {}).get("dovetail_insights")
                or i.get("research_context", {}).get("freshdesk_tickets")
                or i.get("research_context", {}).get("outset_studies")
            ]),
            "triangulated_issues": len([
                i for i in self.issues if i.get("research_context", {}).get("triangulated")
            ]),
            "github_report_url": github_report_url,
            "confluence_weekly_report": weekly_report_url,
            "confluence_issue_pages": len(issue_pages),
            "confluence_space": CONFLUENCE_SPACE
        }


def main():
    try:
        agent = ResearchInsightAgentCloud()
        result = agent.run()

        print(json.dumps(result, indent=2))
        return 0

    except Exception as e:
        print(f"\n❌ Agent failed: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
