# Research Insight Agent - Cursor Edition

A Python agent that runs on a schedule (GitHub Actions), queries PostHog funnel data, Pendo/Dovetail/Freshdesk research, identifies UX drop-offs, synthesizes findings with AI, and publishes **linkable reports** to GitHub Pages and/or Confluence.

**→ See [SETUP.md](./SETUP.md) for GitHub Pages, BigQuery/Freshdesk, and Confluence configuration.**

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

### 3. Test Locally
```bash
python agent_cloud.py
```

You should see output like:
```
🚀 Research Insight Monitor Agent (Cloud Edition)
   Time: 2026-08-27T...
   Week: 2026-08-26

🔍 Querying PostHog funnels...
  ✅ Publisher/Partner Signup Flow
  ✅ Onboarding Checklist
  ...

📊 Analyzing 13 funnels for drop-offs > 15%...
  Found 27 significant drop-offs

✨ Agent run complete!
```

---

## How It Works

### Architecture
```
GitHub Actions (Weekly Schedule)
    ↓
    python agent_cloud.py
    ↓
PostHog + Pendo + Dovetail + Freshdesk (BigQuery) → Analyze → Synthesize
    ↓
Publish to GitHub Pages (linkable) + Confluence (optional)
    ↓
Team bookmarks: https://<org>.github.io/<repo>/
```

### The Agent Pipeline

1. **Query PostHog** (Method: `query_posthog_funnels`)
   - Runs 13 predefined funnels
   - Gets 7-day historical data
   - Returns step counts and conversions

2. **Analyze** (Method: `analyze_funnels`)
   - Finds drop-offs > 15% between funnel steps
   - Calculates severity (HIGH: >30%, MEDIUM: 15-30%)
   - Ranks by user impact

3. **Gather qualitative research**
   - **Pendo** (`query_pendo_feedback`) — open-text poll responses from the last 7 days
   - **Dovetail** (`query_dovetail_insights`) — insights, highlights, and notes
   - **Freshdesk** (`query_freshdesk_support_tickets`) — support tickets via BigQuery
   - **Outset** — no public REST API yet; use Outset MCP in Cursor for interactive access

4. **Enrich** (Method: `enrich_issues_with_research`)
   - Matches Pendo feedback and Dovetail insights to funnel issues by keyword overlap
   - Attaches `research_context` to each issue for synthesis and Confluence pages

5. **Synthesize** (Method: `synthesize_with_gemini`)
   - Uses Google Gemini to explain WHY users drop off
   - Incorporates qualitative research evidence when available
   - Generates 2-3 sentence analysis per issue
   - Fallback to simple metrics if API fails

6. **Publish reports**
   - **GitHub Pages** — HTML + JSON in `docs/research/` (linkable URL)
   - **Confluence** — weekly summary + issue pages (upsert, no duplicates)

---

## File Structure

```
research-agent/
├── agent_cloud.py              # Main agent (506 lines)
├── requirements.txt            # Python dependencies (2 packages)
├── .env.example               # Environment template (copy to .env)
├── .env                       # Actual secrets (in .gitignore)
├── .gitignore                 # What not to commit
├── README.md                  # This file
└── .github/
    └── workflows/
        └── research-agent.yml  # GitHub Actions schedule
```

---

## Environment Variables

**Required:**
- `POSTHOG_API_KEY` – PostHog API key (get from PostHog settings)
- `GOOGLE_API_KEY` – Google Gemini API key
- `CONFLUENCE_URL` – Your Confluence instance URL
- `CONFLUENCE_USERNAME` – Your Atlassian email
- `CONFLUENCE_API_TOKEN` – Confluence API token (create at Atlassian)
- `CONFLUENCE_SPACE` – Confluence space key (e.g., "RESEARCH")

**Optional:**
- `PENDO_API_KEY` – Pendo integration key (Settings → Integrations → Integration Keys)
- `PENDO_SUBSCRIPTION_ID` – Your Pendo subscription ID (reference only)
- `PENDO_REGION` – Pendo region: `US`, `EU`, `US1`, `JPN`, or `AU` (auto-detected from key suffix if omitted)
- `DOVETAIL_API_KEY` – Dovetail personal API token (Settings → Account → Personal API keys)
- `DOVETAIL_BASE_URL` – Dovetail API base URL (default: `https://dovetail.com`)
- `OUTSET_API_KEY` – Reserved; Outset has no public REST API yet (use Outset MCP in Cursor)
- `SLACK_WEBHOOK_URL` – Slack notifications

---

## Key Classes & Methods

### `ResearchInsightAgentCloud`

| Method | Purpose |
|--------|---------|
| `query_posthog_funnels()` | Fetch funnel data from PostHog API |
| `analyze_funnels(results)` | Identify drop-offs >15% |
| `query_pendo_feedback()` | Fetch open-text poll responses from Pendo |
| `query_dovetail_insights(issues)` | Search Dovetail for related research |
| `query_outset_studies()` | Outset placeholder (REST API not available) |
| `enrich_issues_with_research()` | Match qualitative evidence to funnel issues |
| `synthesize_with_gemini(issues)` | Get AI analysis for each issue |
| `create_confluence_weekly_report()` | Create summary page |
| `create_confluence_issue_pages()` | Create individual issue pages |
| `run()` | Execute full pipeline |

### Main Entry Point

```python
agent = ResearchInsightAgentCloud()
result = agent.run()
# Returns: {
#   "timestamp": "2026-08-27T...",
#   "issues_found": 27,
#   "high_severity": 3,
#   "medium_severity": 24,
#   "confluence_weekly_report": "https://...",
#   "confluence_space": "RESEARCH"
# }
```

---

## The 13 Funnels

The agent monitors these key flows:

1. Publisher/Partner Signup Flow
2. Onboarding Checklist
3. Login Flow
4. Contract Browse to Apply ⭐ (high drop-off)
5. UPS (Unified Proposal System) Flow
6. PublisherPro - Link Management
7. Finance/Reporting Access
8. Brand Finance Setup
9. Multi-Link Widget (MLW) Creation
10. Campaign Recruitment Flow
11. Brand Program Marketplace
12. Publisher Settings - Promotional Channels
13. Brand Storefronts Setup

Each funnel is analyzed for drop-offs between steps.

---

## Customization in Cursor

### Add a New Funnel
1. Open `agent_cloud.py`
2. Find `KEY_FUNNELS = [`
3. Add a new dict:
```python
{"name": "Your Funnel Name", "events": [
    "EVENT:step_1_view",
    "EVENT:step_2_view",
    "EVENT:step_3_submit"
]},
```

### Change Drop-off Threshold
Line 33:
```python
DROP_OFF_THRESHOLD = 15  # Change to 10, 20, etc.
```

### Add Custom Synthesis Prompt
Line 232-241 in `synthesize_with_gemini()`:
```python
prompt = f"""... your custom prompt here ..."""
```

### Limit Issues Analyzed
Line 230 (synthesis) and 377 (Confluence):
```python
for issue in issues[:5]:  # Change 5 to 10, 20, etc.
```

---

## Deploying to GitHub Actions

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial Research Agent setup"
git remote add origin https://github.com/YOUR_USERNAME/research-agent.git
git push -u origin main
```

### 2. Add Secrets to GitHub
- Go to Settings → Secrets and variables → Actions
- Click "New repository secret"
- Add each variable from your `.env`:
  - `POSTHOG_API_KEY`
  - `GOOGLE_API_KEY`
  - `CONFLUENCE_URL`
  - `CONFLUENCE_USERNAME`
  - `CONFLUENCE_API_TOKEN`
  - `CONFLUENCE_SPACE`
  - `POSTHOG_PROJECT_ID`

### 3. Verify Workflow
- Go to Actions tab
- Select "Research Insight Agent - Cloud"
- You should see: "scheduled" with cron: `0 7 1 1,4,7,10 *` (quarterly: 1 Jan / Apr / Jul / Oct, 7 AM UTC)
- Or run anytime: **Actions → Research Insight Agent → Run workflow**

### 4. Test Manually
- Click "Run workflow" → "Run workflow"
- Monitor the run (1-2 minutes)
- Check Confluence for results

---

## Debugging

### Run with Verbose Output
```bash
python -u agent_cloud.py 2>&1 | tee agent.log
```

### Test PostHog Connection
```python
import requests
response = requests.post(
    "https://us.posthog.com/api/projects/186875/query/",
    headers={"Authorization": f"Bearer {YOUR_API_KEY}"},
    json={"kind": "FunnelsQuery", "series": [...], "dateRange": {"date_from": "-7d"}}
)
print(response.status_code, response.json())
```

### Test Confluence Connection
```python
import requests
auth = ("your_email@company.com", "YOUR_API_TOKEN")
response = requests.post(
    "https://yourcompany.atlassian.net/wiki/rest/api/content",
    json={...},
    auth=auth
)
print(response.status_code)
```

### Common Errors

| Error | Fix |
|-------|-----|
| `PostHog connection refused` | Normal in GitHub Actions; agent works locally |
| `Invalid Confluence credentials` | Check API token (create new at Atlassian) |
| `No API key provided` | Copy `.env.example` to `.env` and fill in values |
| `Import error: requests` | Run `pip install -r requirements.txt` |

---

## Cursor Tips & Tricks

### 1. Ask Claude About Code
- Highlight any function
- Press `Ctrl+K`
- Ask: "What does this do?" or "How can I modify this?"
- Claude explains and can edit for you

### 2. Generate Code
- Select a line
- Press `Ctrl+K`
- Ask: "Add error handling for the PostHog API call"
- Claude writes it

### 3. Debug with Claude
- Paste error message into chat
- Ask: "Why is this happening?"
- Claude suggests fixes

### 4. Refactor
- Select code block
- Press `Ctrl+K`
- Ask: "Make this more readable"
- Claude improves it

---

## What Happens on Schedule (Quarterly)

```
7:00 AM UTC on 1 Jan, 1 Apr, 1 Jul, 1 Oct
  ↓
GitHub Actions workflow triggered
  ↓
1. Download agent code
2. Install dependencies (requests)
3. Query PostHog for 13 funnels
4. Analyze for drop-offs >15%
5. Synthesize findings with Gemini
6. Create Confluence weekly report page
7. Create individual issue pages
8. Send Slack notification (if enabled)
  ↓
Weekly report appears in Confluence
  ↓
Team reviews findings after each run (or trigger manually when needed)
```

---

## Next Steps

1. ✅ Set up in Cursor (you are here)
2. ✅ Test locally: `python agent_cloud.py`
3. ✅ Add your API keys to `.env`
4. ✅ Push to GitHub
5. ✅ Add GitHub secrets
6. ✅ Wait for next quarterly run, or use **Run workflow** in Actions
7. ✅ Review findings in Confluence
8. ✅ Iterate on funnels & analysis

---

## Support

**If the agent fails:**
- Check GitHub Actions logs (Actions tab → workflow run)
- Verify all secrets are set correctly
- Test locally: `python agent_cloud.py`
- Check Confluence space permissions

**If Confluence pages aren't created:**
- Verify API token is still valid
- Check space key matches `CONFLUENCE_SPACE`
- Ensure URL has no trailing slash

---

## License

Internal use only.

---

**Questions?** Ask Claude in Cursor! Highlight any code and press Ctrl+K.
