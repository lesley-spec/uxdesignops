# Research Insight Agent — Setup

## What changed

The agent now publishes **linkable reports** in two places:

1. **GitHub Pages** (recommended) — stable URL your team can bookmark
2. **Confluence** (optional) — weekly report + issue pages, updated in place

It also pulls **Freshdesk support tickets** from BigQuery (Freshworks datalake).

---

## Quick start

```bash
cd research-agent
cp .env.example .env
# Fill in API keys
python -m pip install -r requirements.txt
python agent_cloud.py
```

After a run, open `docs/research/index.html` locally or deploy via GitHub Actions.

---

## GitHub Pages (linkable report)

### One-time setup

1. Push this repo to GitHub
2. **Settings → Pages → Build and deployment → Source: GitHub Actions**
3. Add repository secrets (see below)
4. Run workflow: **Actions → Research Insight Agent → Run workflow**

### Your shareable URL

```
https://<org>.github.io/<repo>/
```

- Latest report: redirects from `/` to `/reports/YYYY-MM-DD.html`
- Archive: `/reports/` folder with HTML + JSON per week
- Machine-readable: `/latest.json`

Set `GITHUB_PAGES_URL` in `.env` to this URL so the agent prints the public link after each run.

---

## Confluence (optional)

Set in `.env`:

```
PUBLISH_CONFLUENCE=true
CONFLUENCE_URL=https://impact.atlassian.net/wiki
CONFLUENCE_USERNAME=you@impact.com
CONFLUENCE_API_TOKEN=...
CONFLUENCE_SPACE=ux
```

Pages are **upserted** (updated if they already exist) — no duplicate pages on re-runs.

The Confluence weekly report includes a link to the GitHub Pages report when both are enabled.

To use GitHub Pages only:

```
PUBLISH_CONFLUENCE=false
```

---

## Freshdesk / BigQuery

Data source: [BigQuery console](https://console.cloud.google.com/bigquery?project=bt-impact-labs) — `prod-data-enablement.datalake_freshdesk`

### Local auth

```bash
gcloud auth application-default login
gcloud config set project bt-impact-labs
```

### Environment variables

```
BIGQUERY_PROJECT=bt-impact-labs
BIGQUERY_DATASET=prod-data-enablement
BIGQUERY_TICKETS_TABLE=datalake_freshdesk
FRESHDESK_DOMAIN=your-subdomain   # for ticket links
```

If your table path or column names differ, override:

```
BIGQUERY_FRESHDESK_TABLE=bt-impact-labs.prod-data-enablement.your_table_name
```

### GitHub Actions auth

1. Create a GCP service account with **BigQuery Data Viewer** on the dataset
2. Add JSON key as repository secret: `GCP_SA_KEY`

### Verify table schema

In BigQuery console, run:

```sql
SELECT column_name, data_type
FROM `bt-impact-labs.prod-data-enablement.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'datalake_freshdesk'
ORDER BY ordinal_position;
```

If the table name differs, list tables:

```sql
SELECT table_name
FROM `bt-impact-labs.prod-data-enablement.INFORMATION_SCHEMA.TABLES`;
```

Share the correct table/column names if the default query fails — we'll update `freshdesk_bigquery.py`.

---

## GitHub Actions secrets

| Secret | Required | Purpose |
|--------|----------|---------|
| `POSTHOG_API_KEY` | Yes | Funnel drop-off detection |
| `POSTHOG_PROJECT_ID` | Yes | `186875` for Impact Membersite |
| `GOOGLE_API_KEY` | Yes | Gemini synthesis |
| `GCP_SA_KEY` | For Freshdesk | BigQuery service account JSON |
| `CONFLUENCE_*` | Optional | Confluence publishing |
| `PENDO_API_KEY` | Optional | In-app feedback |
| `DOVETAIL_API_KEY` | Optional | Research insights |
| `SLACK_WEBHOOK_URL` | Optional | Run notifications |

### Repository variables (optional)

| Variable | Default |
|----------|---------|
| `BIGQUERY_PROJECT` | `bt-impact-labs` |
| `BIGQUERY_DATASET` | `prod-data-enablement` |
| `BIGQUERY_TICKETS_TABLE` | `datalake_freshdesk` |
| `FRESHDESK_DOMAIN` | your Freshdesk subdomain |

---

## Triangulation

An issue is marked **triangulated** when 2+ independent research sources match (PostHog drop-off + Pendo/Dovetail/Freshdesk). This flags high-confidence problems worth prioritizing in Define.
