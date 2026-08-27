# Cursor Project Bundle - Research Insight Agent

## ✅ Yes, Cursor is Perfect for This

Cursor excels at Python projects like this one because:
- **Native Python support** – syntax highlighting, debugging, refactoring
- **Environment management** – install dependencies, manage .env files
- **Git integration** – push to GitHub directly
- **AI assistance** – edit code with Claude, ask questions inline
- **File structure** – organize your agent, workflows, and config clearly

---

## 📦 Files You Need (Complete List)

Below are **all 4 files** you need to bring into Cursor. Copy each one into a new Cursor project.

### File 1: `agent_cloud.py` (Main Agent)
**Location:** Root of your project  
**Size:** ~18 KB  
**Purpose:** The core Research Insight Agent that queries PostHog, analyzes funnels, and saves to Confluence

```
[Copy the full agent_cloud.py file below]
```

### File 2: `requirements.txt` (Dependencies)
**Location:** Root of your project  
**Size:** 2 lines  
**Purpose:** Lists Python packages needed to run the agent

```
requests>=2.31.0
python-dateutil>=2.8.2
```

### File 3: `.github/workflows/research-agent.yml` (GitHub Actions)
**Location:** `.github/workflows/` subdirectory  
**Size:** ~4 KB  
**Purpose:** Schedules the agent to run every Monday at 7 AM UTC on GitHub

```
[Copy the full workflow file below]
```

### File 4: `.env.example` (Configuration Template)
**Location:** Root of your project  
**Size:** 1 KB  
**Purpose:** Template for environment variables (don't commit real secrets!)

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

### File 5: `README.md` (Documentation)
**Location:** Root of your project  
**Size:** ~3 KB  
**Purpose:** Setup and usage instructions

```
# Research Insight Agent - Cursor Edition

## Quick Start

### 1. Install Dependencies
python -m pip install -r requirements.txt

### 2. Set Up Environment
cp .env.example .env
# Edit .env with your API keys

### 3. Test Locally
python agent_cloud.py

### 4. Deploy to GitHub Actions
- Push to GitHub
- Go to Settings → Secrets → Add your secrets
- Workflow runs every Monday at 7 AM UTC

## What It Does

1. **Queries PostHog** – Analyzes 13 key funnels for drop-offs >15%
2. **Analyzes** – Calculates severity and user impact
3. **Synthesizes** – Uses Google Gemini to explain why users drop off
4. **Saves to Confluence** – Creates weekly reports + individual issue pages

## Project Structure

your-research-agent/
├── agent_cloud.py           # Main agent
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .github/
│   └── workflows/
│       └── research-agent.yml   # GitHub Actions schedule
├── README.md
└── .gitignore              # Don't commit .env!

## Environment Variables

See `.env.example` for all variables needed.

## Debugging

python -u agent_cloud.py
# Shows real-time output with timestamps
```

---

## 🚀 Setup Checklist for Cursor

**Step 1: Create New Project in Cursor**
- [ ] Open Cursor
- [ ] File → New Folder
- [ ] Name: `research-agent` (or your preference)
- [ ] Create these files:

```
research-agent/
├── agent_cloud.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── .github/workflows/research-agent.yml
```

**Step 2: Install Dependencies**
- [ ] Open Terminal in Cursor (Ctrl+`)
- [ ] Run: `python -m pip install -r requirements.txt`
- [ ] Verify: `python -c "import requests; print('✅ OK')"`

**Step 3: Test Locally**
- [ ] Copy `.env.example` to `.env`
- [ ] Add your API keys to `.env`
- [ ] Run: `python agent_cloud.py`
- [ ] Check output for errors

**Step 4: Prepare for GitHub Actions**
- [ ] Create repository on GitHub
- [ ] Push your code: `git push -u origin main`
- [ ] Go to GitHub Settings → Secrets and variables → Actions
- [ ] Add each secret from your `.env`
- [ ] Verify workflow runs on schedule

**Step 5: Monitor & Iterate**
- [ ] Check GitHub Actions tab for workflow runs
- [ ] Review Confluence for weekly reports
- [ ] Iterate on funnel definitions and analysis

---

## 💡 Why Cursor?

| Task | Cursor | vs VS Code |
|------|--------|-----------|
| Edit agent code | ✅ Native + AI | Basic |
| Debug issues | ✅ Inline Claude chat | Manual breakpoints |
| Add new features | ✅ "Add a new funnel" → Claude writes it | Copy/paste templates |
| Push to GitHub | ✅ Terminal + git commands | Terminal + git commands |
| Ask questions | ✅ @Claude while coding | External chat |

---

## 📝 Next Steps in Cursor

1. **Open `agent_cloud.py`**
   - Highlight a function
   - Press Ctrl+K → Ask: "What does this function do?"
   - Claude explains inline

2. **Add a New Funnel**
   - In `agent_cloud.py`, find `KEY_FUNNELS`
   - Cursor → "Add a new funnel for the onboarding flow"
   - Claude writes it for you

3. **Customize Analysis**
   - Change `DROP_OFF_THRESHOLD` from 15% to 10% (or whatever you want)
   - Ask Claude: "How do I add revenue impact calculation?"
   - Iterate rapidly

4. **Deploy Changes**
   - Test locally: `python agent_cloud.py`
   - Push to GitHub
   - Actions runs automatically

---

## 🔗 Files Ready to Copy

All files below are ready to copy into Cursor. Create them in this order:

1. `requirements.txt` (2 lines)
2. `.env.example` (10 lines)
3. `agent_cloud.py` (506 lines)
4. `.github/workflows/research-agent.yml` (92 lines)
5. `README.md` (60 lines)
6. `.gitignore` (2 lines)
