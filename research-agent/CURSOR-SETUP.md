# Set Up Research Agent in Cursor - Complete Checklist

## 📋 What You're Building

A Python agent that:
- Runs on schedule (GitHub Actions, every Monday 7 AM UTC)
- Queries PostHog for funnel data
- Analyzes for UX drop-offs >15%
- Uses Google Gemini to explain issues
- Saves findings to Confluence (searchable, discoverable)

**Time to set up:** 10-15 minutes  
**Difficulty:** Easy (Python + config files)  
**Best in Cursor because:** Native Python, inline AI help, terminal access

---

## 🎯 Step-by-Step Setup

### Step 1: Create Project in Cursor
- [ ] Open Cursor
- [ ] File → Open Folder
- [ ] Create new folder: `research-agent`
- [ ] Open this folder in Cursor

### Step 2: Create File Structure
Inside `research-agent/`, create these files in this order:

#### 2.1 Create `requirements.txt`
File → New File → `requirements.txt`

Copy this exactly:
```
requests>=2.31.0
python-dateutil>=2.8.2
```

#### 2.2 Create `.env.example`
File → New File → `.env.example`

Copy this (template, don't add real keys yet):
```
# PostHog Configuration
POSTHOG_PROJECT_ID=186875
POSTHOG_API_KEY=your_posthog_api_key_here

# Google Gemini (AI Synthesis)
GOOGLE_API_KEY=your_google_api_key_here

# Confluence (Storage)
CONFLUENCE_URL=https://yourcompany.atlassian.net/wiki
CONFLUENCE_USERNAME=your_email@company.com
CONFLUENCE_API_TOKEN=your_confluence_api_token_here
CONFLUENCE_SPACE=RESEARCH

# Optional
PENDO_API_KEY=
OUTSET_API_KEY=
DOVETAIL_API_KEY=
SLACK_WEBHOOK_URL=
```

#### 2.3 Create `.gitignore`
File → New File → `.gitignore`

Copy this (protects your secrets):
```
# Environment variables (never commit!)
.env
.env.local

# Python
__pycache__/
*.py[cod]
*.egg-info/
venv/
env/

# IDE
.vscode/
.idea/
*.swp
.DS_Store

# Logs
*.log
```

#### 2.4 Create `agent_cloud.py`
File → New File → `agent_cloud.py`

Copy the entire file from the section below ⬇️

#### 2.5 Create Workflow File
Right-click → New Folder → `.github`  
Right-click → New Folder → `workflows`  
File → New File → `research-agent.yml`

Copy the entire file from the section below ⬇️

#### 2.6 Create `README.md`
File → New File → `README.md`

Copy the entire file from the section below ⬇️

### Step 3: Install Dependencies
- [ ] Terminal → New Terminal (Ctrl+`)
- [ ] Run: `python -m pip install -r requirements.txt`
- [ ] Wait for completion

### Step 4: Create `.env` (with real keys)
- [ ] Copy `.env.example` to `.env`:
  ```bash
  cp .env.example .env
  ```
- [ ] Open `.env` in Cursor
- [ ] Add your real API keys:
  - `POSTHOG_API_KEY` – from PostHog
  - `GOOGLE_API_KEY` – from Google Cloud
  - `CONFLUENCE_*` – from Atlassian
- [ ] Don't commit `.env` (it's in .gitignore)

### Step 5: Test Locally
- [ ] Terminal: `python agent_cloud.py`
- [ ] You should see:
  ```
  🚀 Research Insight Monitor Agent
  🔍 Querying PostHog funnels...
  📊 Analyzing funnels...
  ✨ Agent run complete!
  ```

### Step 6: Push to GitHub
- [ ] Terminal: `git init`
- [ ] Terminal: `git add .`
- [ ] Terminal: `git commit -m "Initial setup"`
- [ ] Create repo on GitHub (github.com/new)
- [ ] Terminal: `git remote add origin https://github.com/YOUR_USER/research-agent.git`
- [ ] Terminal: `git push -u origin main`

### Step 7: Add GitHub Secrets
- [ ] Go to GitHub repo
- [ ] Settings → Secrets and variables → Actions
- [ ] Click "New repository secret" for each:
  - `POSTHOG_PROJECT_ID` = `186875`
  - `POSTHOG_API_KEY` = (from your `.env`)
  - `GOOGLE_API_KEY` = (from your `.env`)
  - `CONFLUENCE_URL` = (from your `.env`)
  - `CONFLUENCE_USERNAME` = (from your `.env`)
  - `CONFLUENCE_API_TOKEN` = (from your `.env`)
  - `CONFLUENCE_SPACE` = `RESEARCH`

### Step 8: Test Workflow
- [ ] Go to GitHub → Actions tab
- [ ] Select "Research Insight Agent - Cloud"
- [ ] Click "Run workflow" → "Run workflow"
- [ ] Wait 1-2 minutes
- [ ] Check logs for success
- [ ] Check Confluence for weekly report page

### Step 9: Verify Results
- [ ] Go to Confluence
- [ ] Navigate to "Research & Insights" space
- [ ] You should see:
  - ✅ "Weekly Report: Week of 2026-08-26" (summary page)
  - ✅ Individual issue pages (one per high drop-off)
  - ✅ All pages tagged with [research], [high], etc.

---

## 📁 Final Project Structure

When complete, your Cursor project should look like this:

```
research-agent/
├── agent_cloud.py              ← Main agent (copy below)
├── requirements.txt            ← Dependencies (copy below)
├── .env.example               ← Template (copy below)
├── .env                       ← Your secrets (create from .env.example)
├── .gitignore                 ← Git rules (copy below)
├── README.md                  ← Docs (copy below)
└── .github/
    └── workflows/
        └── research-agent.yml  ← GitHub Actions (copy below)
```

---

## 📝 Files to Copy into Cursor

### File 1: `agent_cloud.py`
[See main file list in this project - it's the long Python file]

**Location in Cursor:** Root  
**Size:** ~506 lines  
**How to get it:** The full content is in `/home/claude/agent_cloud.py` in this session

### File 2: `requirements.txt`
```
requests>=2.31.0
python-dateutil>=2.8.2
```

**Location in Cursor:** Root  
**Size:** 2 lines

### File 3: `.env.example`
[See above in Step 2.2]

**Location in Cursor:** Root  
**Size:** ~20 lines

### File 4: `.gitignore`
[See above in Step 2.3]

**Location in Cursor:** Root  
**Size:** ~15 lines

### File 5: `research-agent.yml`
[See main file list - it's the GitHub Actions workflow]

**Location in Cursor:** `.github/workflows/`  
**Size:** ~92 lines

### File 6: `README.md`
[See the comprehensive README provided]

**Location in Cursor:** Root  
**Size:** ~200 lines

---

## ✅ Verification Checklist

After setup, verify everything works:

**Local Testing:**
- [ ] `python -m pip install -r requirements.txt` ← No errors
- [ ] `python agent_cloud.py` ← Runs and completes
- [ ] `.env` file exists and has your real keys
- [ ] No `.env` is committed (check .gitignore works)

**GitHub Setup:**
- [ ] Repo exists on GitHub
- [ ] `.github/workflows/research-agent.yml` is committed
- [ ] 7 secrets are added in Settings → Secrets
- [ ] Workflow runs (manual trigger works)

**Confluence:**
- [ ] Confluence space "Research & Insights" exists
- [ ] Weekly report page was created
- [ ] Issue pages were created
- [ ] All pages are tagged and searchable

---

## 🚀 Using Cursor Effectively

### Get Help from Claude
- Highlight code → Ctrl+K → Ask questions
- Example: "What does query_posthog_funnels do?"
- Claude explains right there

### Generate Code
- Type a comment about what you want
- Cursor → "Generate" or Ctrl+K
- Example: "# Add error handling for the Confluence API"

### Debug Issues
- Terminal shows error?
- Copy the error → Ctrl+K → Paste error
- Ask: "Why is this happening?"
- Claude debugs it

### Modify Agent
- Change `DROP_OFF_THRESHOLD` from 15 to 10 ← Lower threshold
- Add new funnel in `KEY_FUNNELS` → Ask Claude to write it
- Customize the Gemini prompt → Edit the prompt in `synthesize_with_gemini()`

---

## 🔄 Weekly Workflow

Once deployed:

**Every Monday at 7 AM UTC:**
1. GitHub Actions triggers automatically
2. Agent runs, queries PostHog
3. Analyzes funnels, synthesizes findings
4. Creates/updates Confluence pages
5. Sends Slack notification (if enabled)

**Your team:**
1. Checks Slack notification Monday morning
2. Opens Confluence
3. Reviews weekly report and issue pages
4. Links findings to PRDs/design docs

---

## 💡 Quick Tips

| Task | How | In Cursor |
|------|-----|-----------|
| Edit agent code | Open `agent_cloud.py` | Direct edit, with AI help |
| Add new funnel | Edit `KEY_FUNNELS` list | Highlight → Ctrl+K → "Add funnel" |
| Change threshold | Edit line 33 | Change `15` to any number |
| Debug failure | Check `.github/workflows/` logs | Terminal → GitHub Actions |
| Update API keys | Edit `.env` | Never commit `.env`! |
| Test quickly | `python agent_cloud.py` | Terminal in Cursor |

---

## ❓ Troubleshooting

**"ModuleNotFoundError: requests"**
→ Run: `pip install -r requirements.txt`

**"Invalid Confluence credentials"**
→ Create new API token at https://id.atlassian.com/manage-profile/security/api-tokens

**"PostHog connection refused in GitHub Actions"**
→ Normal! It works locally. The workflow runs but may have network limits. This is why we test locally first.

**".env not being read"**
→ Confirm it exists and is not in `.gitignore`. Don't commit it!

**"Workflow not running on schedule"**
→ Check `.github/workflows/research-agent.yml` cron: `0 7 * * 1` means Monday 7 AM UTC. Adjust if needed.

---

## 📞 Next Steps After Setup

1. ✅ Cursor setup (you are here)
2. ✅ Local testing passes
3. ✅ GitHub Actions runs manually
4. ✅ First Confluence pages created
5. ⏭️ **Monday:** Wait for automatic run
6. ⏭️ **Review findings** in Confluence
7. ⏭️ **Iterate:** Adjust funnels, thresholds, synthesis

---

## 🎉 Success Looks Like

When everything works:
- ✅ `python agent_cloud.py` runs without errors
- ✅ Workflow runs in GitHub Actions
- ✅ Confluence pages appear every Monday
- ✅ Team can search and find issues
- ✅ Data flows automatically, no manual work

**You now have an automated research infrastructure.** 🚀

---

**Questions?** Open any file in Cursor, highlight something, press Ctrl+K, and ask Claude!
