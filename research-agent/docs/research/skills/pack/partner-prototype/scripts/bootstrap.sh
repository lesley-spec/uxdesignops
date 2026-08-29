#!/usr/bin/env bash
# partner-prototype bootstrap — clone Partner UI shell, install toolchain + deps, start Vite.
# Agent runs ONE command. Designers should not need git/npm/Node knowledge.
# Node 18+ is auto-provisioned via ensure-toolchain.sh when missing.
set -euo pipefail

REPO_URL="${PARTNER_PROTOTYPE_REPO:-https://github.com/lesley-spec/PartnerUI-shell.git}"
DIR_NAME="${PARTNER_PROTOTYPE_DIR:-partner-ui}"
PARENT="${IMPACT_PROTOTYPE_HOME:-$HOME/Documents/impact-prototypes}"
PROJECT="$PARENT/$DIR_NAME"
START_DEV=1
FORCE_RECLONE=0

usage() {
  cat <<'EOF'
Usage: bootstrap.sh [--no-dev] [--reclone] [--parent DIR]

  Clones the Partner UI prototype template, installs deps, prints READY.

  --no-dev     Skip starting the Vite dev server
  --reclone    Delete existing project folder and clone fresh
  --parent DIR Override IMPACT_PROTOTYPE_HOME (default: ~/Documents/impact-prototypes)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-dev) START_DEV=0; shift ;;
    --reclone) FORCE_RECLONE=1; shift ;;
    --parent) PARENT="$2"; PROJECT="$PARENT/$DIR_NAME"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage >&2; exit 2 ;;
  esac
done

die() { echo "ERROR: $*" >&2; exit 1; }
info() { echo "→ $*"; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "Missing required command: $1
Install it, then re-run: use partner-prototype"
}

need_cmd git

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=ensure-toolchain.sh
. "$SCRIPT_DIR/ensure-toolchain.sh"
impact_ensure_node

mkdir -p "$PARENT"

if [[ "$FORCE_RECLONE" -eq 1 && -e "$PROJECT" ]]; then
  info "Removing existing $PROJECT (--reclone)"
  rm -rf "$PROJECT"
fi

if [[ -d "$PROJECT/.git" ]]; then
  info "Existing project found — updating $PROJECT"
  git -C "$PROJECT" remote set-url origin "$REPO_URL" || true
  if ! git -C "$PROJECT" pull --ff-only origin HEAD 2>/dev/null; then
    info "Fast-forward pull skipped (local changes or divergent history). Using existing checkout."
  fi
elif [[ -e "$PROJECT" ]]; then
  die "Path exists but is not a git repo: $PROJECT
Move/rename it, or re-run with --reclone"
else
  info "Cloning Partner UI template…"
  info "From: $REPO_URL"
  git clone --depth 1 "$REPO_URL" "$PROJECT"
fi

cd "$PROJECT"

if [[ -f package.json ]]; then
  if [[ -f package-lock.json ]]; then
    info "Installing dependencies (npm ci)…"
    npm ci || {
      info "npm ci failed — falling back to npm install"
      npm install
    }
  else
    info "Installing dependencies (npm install)…"
    npm install
  fi
  impact_verify_vite
else
  die "No package.json in $PROJECT — template looks broken. Check $REPO_URL"
fi

_UX_MAKE="$(cd "$SCRIPT_DIR/../../ux-prototyping/scripts" 2>/dev/null && pwd || true)"
if [[ -n "${_UX_MAKE:-}" && -f "$_UX_MAKE/write-figma-make-config.sh" ]]; then
  bash "$_UX_MAKE/write-figma-make-config.sh" --shell partner --project "$PROJECT" || true
fi

PORT="${PARTNER_PROTOTYPE_PORT:-5173}"
DEV_URL="http://localhost:${PORT}/"
if [[ "$START_DEV" -eq 1 ]]; then
  if lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    info "Port $PORT already in use — assuming dev server is running."
  else
    info "Starting Vite on port $PORT (npm run dev)…"
    nohup npm run dev -- --host 127.0.0.1 --port "$PORT" \
      >"$PROJECT/.partner-prototype-dev.log" 2>&1 &
    echo $! >"$PROJECT/.partner-prototype-dev.pid"
    for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
      if lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
        break
      fi
      sleep 0.5
    done
  fi
fi

cat <<EOF

═══════════════════════════════════════════════════════════
 PARTNER PROTOTYPE READY
═══════════════════════════════════════════════════════════
 Path:  $PROJECT
 Repo:  $REPO_URL
 Dev:   $DEV_URL
 Log:   $PROJECT/.partner-prototype-dev.log  (if server started)

 Next for designers:
  1. Open this folder in Cursor (agent should move workspace here)
  2. Open $DEV_URL in the browser
  3. Paste mock Figma links / ask AI to build screens into this shell

IMPACT_PROTOTYPE_READY shell=partner path=$PROJECT url=$DEV_URL
═══════════════════════════════════════════════════════════
EOF
