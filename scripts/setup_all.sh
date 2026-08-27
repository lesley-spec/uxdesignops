#!/usr/bin/env bash
# One-command setup for Research Insight Monitor Agent
# Usage: ./scripts/setup_all.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/research-agent/.env"

echo "=== Research Insight Monitor — setup ==="
echo ""

# 1. Python deps
echo "→ Installing Python dependencies..."
python3 -m pip install -q -r "$ROOT/research-agent/requirements.txt"

# 2. Config check
echo ""
echo "→ Checking configuration..."
python3 "$ROOT/research-agent/scripts/check_setup.py" || true

# 3. Git
if [[ ! -d "$ROOT/.git" ]]; then
  echo "→ Initializing git..."
  git -C "$ROOT" init -b main
fi

# 4. GitHub CLI
if ! gh auth status &>/dev/null; then
  echo ""
  echo "⚠️  GitHub CLI not authenticated."
  echo "   Run:  gh auth login"
  echo "   Then re-run this script to push and set secrets."
else
  echo ""
  echo "→ GitHub authenticated as: $(gh api user -q .login)"

  # Commit if needed
  if [[ -n "$(git -C "$ROOT" status --porcelain)" ]]; then
    echo "→ Committing changes..."
    git -C "$ROOT" add .github .gitignore GETTING_STARTED.md research-agent
    git -C "$ROOT" commit -m "Add Research Insight Monitor agent and GitHub Pages publishing" || true
  fi

  # Create/push repo
  REPO="${GITHUB_REPO:-lesley-spec/uxdesignops}"
  if ! gh repo view "$REPO" &>/dev/null; then
    echo "→ Creating GitHub repo $REPO..."
    gh repo create "$REPO" --private --source="$ROOT" --remote=origin --push
  else
    echo "→ Pushing to $REPO..."
    git -C "$ROOT" remote add origin "git@github.com:$REPO.git" 2>/dev/null || true
    git -C "$ROOT" push -u origin main 2>/dev/null || git -C "$ROOT" push -u origin main
  fi

  # Push secrets from .env
  if [[ -f "$ENV_FILE" ]]; then
    echo "→ Syncing GitHub secrets from .env..."
    "$ROOT/scripts/push_github_secrets.py" || true
  fi

  echo ""
  echo "→ Enable GitHub Pages: Settings → Pages → Source: GitHub Actions"
  echo "→ Run workflow: gh workflow run research-agent.yml"
fi

# 5. gcloud (optional)
if command -v gcloud &>/dev/null; then
  if ! gcloud auth application-default print-access-token &>/dev/null 2>&1; then
    echo ""
    echo "⚠️  GCP not authenticated locally (optional)."
    echo "   Fix gcloud Python: brew install python@3.11"
    echo "   export CLOUDSDK_PYTHON=\$(brew --prefix python@3.11)/bin/python3.11"
    echo "   gcloud auth application-default login"
  else
    echo ""
    echo "→ Discovering BigQuery tables..."
    cd "$ROOT/research-agent" && python3 scripts/discover_bigquery.py || true
  fi
fi

echo ""
echo "=== Next: add missing keys to research-agent/.env ==="
echo "  POSTHOG_API_KEY  → https://us.posthog.com/project/186875/settings/user-api-keys"
echo "  GOOGLE_API_KEY   → https://aistudio.google.com/apikey"
echo "  CONFLUENCE_API_TOKEN → https://id.atlassian.com/manage-profile/security/api-tokens"
echo ""
echo "Then run:  cd research-agent && python3 agent_cloud.py"
echo "Report URL: https://lesley-spec.github.io/uxdesignops/"
