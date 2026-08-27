#!/usr/bin/env bash
# Local BigQuery auth for Freshdesk datalake (uses your @impact.com Google login)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON311="/opt/homebrew/opt/python@3.11/bin/python3.11"

if [[ ! -x "$PYTHON311" ]]; then
  echo "Installing Python 3.11 for gcloud..."
  brew install python@3.11
fi

export CLOUDSDK_PYTHON="$PYTHON311"
export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"

echo "→ Using Python: $CLOUDSDK_PYTHON"
gcloud version | head -1

echo ""
echo "→ Logging in with your Google account (browser will open)..."
echo "  Use the same account that can view bt-impact-labs in BigQuery console."
gcloud auth application-default login --project=bt-impact-labs

gcloud config set project bt-impact-labs

echo ""
echo "→ Installing Python deps (3.11)..."
"$PYTHON311" -m pip install -q -r "$ROOT/research-agent/requirements.txt"

echo ""
echo "→ Discovering BigQuery tables..."
cd "$ROOT/research-agent"
"$PYTHON311" scripts/discover_bigquery.py

echo ""
echo "→ Testing Freshdesk query..."
"$PYTHON311" - <<'PY'
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(".env"))
from freshdesk_bigquery import query_freshdesk_tickets
tickets = query_freshdesk_tickets()
print(f"Sample: {len(tickets)} tickets")
if tickets:
    print(f"  Latest: {tickets[0].get('subject', '')[:80]}")
PY

echo ""
echo "✅ Done. Run the full agent:"
echo "   cd research-agent && python3.11 agent_cloud.py"
echo ""
echo "Tip: add to ~/.zshrc so gcloud keeps working:"
echo '   export CLOUDSDK_PYTHON="/opt/homebrew/opt/python@3.11/bin/python3.11"'
