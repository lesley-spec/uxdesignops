# Getting started — Research Monitor Agent

End-to-end checklist to go from this repo to a **linkable weekly UX research report**.

---

## What you have today

| Piece | Status |
|-------|--------|
| Agent code (PostHog, Pendo, Dovetail, Freshdesk/BQ, synthesis) | Ready |
| GitHub Pages publisher | Ready — reports in `research-agent/docs/research/` |
| Confluence upsert | Ready — needs API token |
| GitHub Actions workflow | Ready — `.github/workflows/research-agent.yml` |
| Git repo | Initialized locally — not pushed yet |
| Dovetail API key | Configured in `.env` |
| PostHog / Gemini / Confluence | **You need to add keys** |

---

## Phase 1 — API keys (15 min)

Edit `research-agent/.env` (never commit this file).

### Required for a full run

1. **PostHog** — [Personal API keys](https://us.posthog.com/project/186875/settings/user-api-keys)  
   → `POSTHOG_API_KEY`

2. **Google Gemini** — [AI Studio](https://aistudio.google.com/apikey)  
   → `GOOGLE_API_KEY` (powers weekly synthesis)

### Recommended

3. **Confluence** — [Atlassian API token](https://id.atlassian.com/manage-profile/security/api-tokens)  
   → `CONFLUENCE_API_TOKEN`  
   Already set: `CONFLUENCE_URL`, `CONFLUENCE_USERNAME`, `CONFLUENCE_SPACE=ux` (Impact UX)

4. **Freshdesk links** — your Freshdesk subdomain  
   → `FRESHDESK_DOMAIN=yourcompany` (ticket URLs in the report)

### Optional

- **Pendo** — `PENDO_API_KEY`, `PENDO_SUBSCRIPTION_ID`
- **Outset** — `OUTSET_API_KEY`

Validate:

```bash
python3 research-agent/scripts/check_setup.py
```

---

## Phase 2 — Push to GitHub (10 min)

```bash
# 1. Log in (one time)
gh auth login

# 2. Create repo and push (adjust org/name if needed)
cd /Users/lesleylinnett/Documents/GitHub/ux-designops-ai
git add .github .gitignore research-agent
git commit -m "Add Research Insight Monitor agent and GitHub Pages publishing"
gh repo create lesley-spec/uxdesignops --private --source=. --push
# Or if repo already exists:
# git remote add origin git@github.com:lesley-spec/uxdesignops.git
# git push -u origin main
```

---

## Phase 3 — GitHub secrets (10 min)

In **GitHub → Settings → Secrets and variables → Actions**, add:

| Secret | Value |
|--------|--------|
| `POSTHOG_PROJECT_ID` | `186875` |
| `POSTHOG_API_KEY` | from PostHog |
| `GOOGLE_API_KEY` | from Google AI Studio |
| `CONFLUENCE_URL` | `https://impact.atlassian.net/wiki` |
| `CONFLUENCE_USERNAME` | `lesley@impact.com` |
| `CONFLUENCE_API_TOKEN` | from Atlassian |
| `CONFLUENCE_SPACE` | `ux` |
| `DOVETAIL_API_KEY` | same as in `.env` |
| `DOVETAIL_BASE_URL` | `https://dovetail.com` |
| `GCP_SA_KEY` | GCP service account JSON (BigQuery read on `bt-impact-labs`) |

Optional: `PENDO_*`, `OUTSET_API_KEY`, `FRESHDESK_DOMAIN`

---

## Phase 4 — Enable GitHub Pages (2 min)

1. **Settings → Pages → Build and deployment**
2. Source: **GitHub Actions**
3. After first workflow run, your report URL:

   **https://lesley-spec.github.io/uxdesignops/**

   (Update `GITHUB_PAGES_URL` in `.env` if org/repo name differs.)

---

## Phase 5 — BigQuery / Freshdesk (CI or local)

**In CI:** `GCP_SA_KEY` secret is enough — workflow authenticates automatically.

**Locally** (optional):

```bash
# gcloud needs Python 3.10+
brew install python@3.11
export CLOUDSDK_PYTHON=$(brew --prefix python@3.11)/bin/python3.11
gcloud auth application-default login

# Discover table schema
python3 research-agent/scripts/discover_bigquery.py
```

Table: `bt-impact-labs.prod-data-enablement.datalake_freshdesk`

---

## Phase 6 — Run it

**Local:**

```bash
cd research-agent
python3 -m pip install -r requirements.txt
python3 agent_cloud.py
open docs/research/index.html          # Pipeline home
open docs/research/research/index.html  # Research listing
```

**CI:** Actions → **Research Insight Agent** → **Run workflow**

Runs automatically **quarterly** (1 Jan, 1 Apr, 1 Jul, 1 Oct at 7:00 UTC), or trigger manually anytime from **Actions → Research Insight Agent → Run workflow**.

---

## Phase 5 — Protect the site (@impact.com Google login)

The GitHub Pages site uses a **Google sign-in gate** restricted to `@impact.com` accounts.

### One-time setup

1. **Google Cloud Console** → [APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials)
2. Create **OAuth 2.0 Client ID** → Application type: **Web application**
3. **Authorized JavaScript origins:**
   - `https://lesley-spec.github.io`
4. Copy the **Client ID** (ends in `.apps.googleusercontent.com`)
5. Add GitHub repo secret:
   ```bash
   gh secret set GOOGLE_OAUTH_CLIENT_ID --body "YOUR_CLIENT_ID.apps.googleusercontent.com"
   ```
6. Redeploy Pages (push any change under `research-agent/docs/research/` or run **Deploy Research Report to GitHub Pages** workflow)

### Behavior

- Visitors see a sign-in screen until they authenticate with Google
- Only `@impact.com` emails (e.g. `lesley@impact.com`) can view the site
- Others see: **You don't have permission to view this**
- Session lasts 24 hours in the browser tab

**Note:** GitHub Pages is static hosting — direct URLs like `/latest.json` can still be fetched without the UI gate. For strict enterprise lockdown, add [Cloudflare Access](https://developers.cloudflare.com/cloudflare-one/policies/access/) or similar in front of the domain.

---

## What success looks like

After a successful run you get:

- **Public report:** `https://lesley-spec.github.io/uxdesignops/v1/reports/YYYY-MM-DD.html`
- **Latest JSON:** `.../latest.json`
- **Confluence page** in [Impact UX](https://impact.atlassian.net/wiki/spaces/ux) space (if token set)
- Console output with issue counts, triangulation flags, and share link

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| 0 issues found | Add `POSTHOG_API_KEY`; agent needs PostHog for funnel drop-offs |
| No shareable URL printed | Set `GITHUB_PAGES_URL` in `.env`; push and enable Pages |
| BigQuery auth failed locally | Use CI + `GCP_SA_KEY`, or fix gcloud Python version |
| Confluence skipped | Set `CONFLUENCE_API_TOKEN` |
| Empty Freshdesk section | Verify GCP access + table name; run `discover_bigquery.py` |

Run `python3 research-agent/scripts/check_setup.py` anytime for a status snapshot.

More detail: [research-agent/SETUP.md](research-agent/SETUP.md)
