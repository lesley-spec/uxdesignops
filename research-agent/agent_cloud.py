#!/usr/bin/env python3
"""
Research Insight Monitor Agent - Cloud Edition
Runs in GitHub Actions and publishes a filterable HTML report to GitHub Pages.
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

from dovetail_api import query_dovetail_items
from freshdesk_bigquery import query_freshdesk_tickets
from issue_taxonomy import select_top_issues, tag_issues
from outset_api import query_outset_studies as fetch_outset_studies
from pendo_api import query_pendo_items as fetch_pendo_items
from posthog_api import query_posthog_dropoffs
from report_publisher import build_report_payload, publish_github_pages_report

# Configuration from environment variables
POSTHOG_PROJECT_ID = os.environ.get("POSTHOG_PROJECT_ID", "186875")
POSTHOG_API_KEY = os.environ.get("POSTHOG_API_KEY", "")
POSTHOG_BASE_URL = "https://us.posthog.com"

PENDO_API_KEY = os.environ.get("PENDO_API_KEY", "")
PENDO_SUBSCRIPTION_ID = os.environ.get("PENDO_SUBSCRIPTION_ID", "")
PENDO_REGION = os.environ.get("PENDO_REGION", "US").upper()

RESEARCH_STOPWORDS = {
    "flow", "the", "and", "for", "with", "from", "step", "drop", "off", "to", "a", "an",
}

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
SYNTHESIS_MODEL = os.environ.get("SYNTHESIS_MODEL", "google")

PUBLISH_GITHUB_PAGES = os.environ.get("PUBLISH_GITHUB_PAGES", "true").lower() not in {"0", "false", "no"}
GITHUB_PAGES_URL = os.environ.get("GITHUB_PAGES_URL", "")

DROP_OFF_THRESHOLD = 15
TOP_ISSUES_LIMIT = int(os.environ.get("TOP_ISSUES_PER_WEEK", "20"))
REPORT_LOOKBACK_DAYS = int(os.environ.get("REPORT_LOOKBACK_DAYS", "90"))


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

    def query_pendo_data(self):
        """Fetch Pendo poll feedback and product analytics."""
        return fetch_pendo_items(lookback_days=REPORT_LOOKBACK_DAYS)

    def query_outset_studies(self) -> List[Dict]:
        """Fetch studies from Outset REST API."""
        return fetch_outset_studies()

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
                bool(matched_outset),
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
        model = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")

        for issue in issues[:TOP_ISSUES_LIMIT]:
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

                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
                headers = {
                    "Content-Type": "application/json",
                    "x-goog-api-key": GOOGLE_API_KEY,
                }
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }

                response = requests.post(url, json=payload, headers=headers, timeout=60)
                response.raise_for_status()

                data = response.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    synthesis[issue["title"]] = text
                    print(f"  ✅ {issue['funnel_name']}")

            except Exception as e:
                err = str(e).split("?key=")[0] if "?key=" in str(e) else str(e)
                print(f"  ⚠️  Synthesis error for {issue['funnel_name']}: {err}")
                synthesis[issue["title"]] = f"Drop-off detected: {issue['drop_percentage']}% of users affected"

        return synthesis

    def mock_synthesis(self, issues: List[Dict]) -> Dict[str, str]:
        """Fallback synthesis without API"""
        synthesis = {}
        for issue in issues[:TOP_ISSUES_LIMIT]:
            synthesis[issue["title"]] = (
                f"{issue['drop_percentage']}% drop-off detected. "
                f"{issue['users_affected']} users affected."
            )
        return synthesis

    def run(self) -> Dict:
        """Execute full agent pipeline"""
        print("="*70)
        print("🚀 Research Insight Monitor Agent (Cloud Edition)")
        print("="*70)
        print(f"   Time: {datetime.utcnow().isoformat()}")
        print(f"   Period: last {REPORT_LOOKBACK_DAYS} days (~3 months)")
        print(f"   Week: {self.week_start}")

        # Step 1–2: PostHog — all drop-offs in period; top N for AI synthesis
        all_posthog_issues = query_posthog_dropoffs(lookback_days=REPORT_LOOKBACK_DAYS)
        top_issues = select_top_issues(all_posthog_issues, TOP_ISSUES_LIMIT)
        if len(all_posthog_issues) > len(top_issues):
            print(
                f"  📌 AI synthesis on top {len(top_issues)} of "
                f"{len(all_posthog_issues)} drop-offs"
            )

        # Step 3: Gather qualitative research from other sources
        pendo_feedback, pendo_analytics = self.query_pendo_data()
        dovetail_insights = query_dovetail_items(lookback_days=REPORT_LOOKBACK_DAYS)
        freshdesk_tickets = self.query_freshdesk_support_tickets()
        outset_studies = self.query_outset_studies()

        # Step 4: Enrich all PostHog drop-offs with research context
        all_posthog_issues = self.enrich_issues_with_research(
            all_posthog_issues, pendo_feedback, dovetail_insights, freshdesk_tickets, outset_studies
        )
        all_posthog_issues = tag_issues(all_posthog_issues)
        self.issues = all_posthog_issues

        top_titles = {issue["title"] for issue in top_issues}
        top_for_synthesis = [i for i in all_posthog_issues if i["title"] in top_titles]

        # Step 5: Synthesize with Gemini (top issues only)
        synthesis = self.synthesize_with_gemini(top_for_synthesis)

        # Step 6: Publish filterable HTML report (GitHub Pages)
        github_report_url = None
        if PUBLISH_GITHUB_PAGES:
            print("\n🌐 Publishing HTML report...")
            payload = build_report_payload(
                week_start=self.week_start,
                posthog_dropoffs=all_posthog_issues,
                synthesis=synthesis,
                pendo_feedback=pendo_feedback,
                pendo_analytics=pendo_analytics,
                dovetail_insights=dovetail_insights,
                freshdesk_tickets=freshdesk_tickets,
                outset_studies=outset_studies,
                top_issues_limit=TOP_ISSUES_LIMIT,
                lookback_days=REPORT_LOOKBACK_DAYS,
            )
            github_report_url = publish_github_pages_report(payload)

        if github_report_url:
            print(f"\n🔗 Share this report: {github_report_url}")

        print("\n" + "="*70)
        print("✨ Agent run complete!")
        print("="*70)

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "week": self.week_start,
            "issues_found": len(all_posthog_issues),
            "high_severity": len([i for i in all_posthog_issues if i["severity"] == "HIGH"]),
            "medium_severity": len([i for i in all_posthog_issues if i["severity"] == "MEDIUM"]),
            "pendo_feedback_count": len(pendo_feedback),
            "pendo_analytics_count": len(pendo_analytics),
            "dovetail_insights_count": len(dovetail_insights),
            "freshdesk_tickets_count": len(freshdesk_tickets),
            "outset_studies_count": len(outset_studies),
            "issues_with_research_context": len([
                i for i in all_posthog_issues
                if i.get("research_context", {}).get("pendo_feedback")
                or i.get("research_context", {}).get("dovetail_insights")
                or i.get("research_context", {}).get("freshdesk_tickets")
                or i.get("research_context", {}).get("outset_studies")
            ]),
            "triangulated_issues": len([
                i for i in all_posthog_issues if i.get("research_context", {}).get("triangulated")
            ]),
            "ai_synthesized_count": len(synthesis),
            "github_report_url": github_report_url,
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
