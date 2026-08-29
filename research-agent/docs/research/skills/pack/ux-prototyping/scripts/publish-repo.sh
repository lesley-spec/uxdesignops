#!/usr/bin/env bash
# ux-prototyping — push the running prototype as a NEW repo on the logged-in
# GitHub user (or an org they can create in) and enable GitHub Pages.
# Never push to the Brand/Partner template remotes.
set -euo pipefail

die() { echo "ERROR: $*" >&2; exit 1; }
info() { echo "→ $*"; }

PROJECT=""
REPO_NAME=""
OWNER="${IMPACT_PROTOTYPE_GITHUB_OWNER:-}"
VISIBILITY="public"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage: publish-repo.sh --project DIR --name REPO [--owner USER_OR_ORG] [--private]

  Creates a new GitHub repo for the logged-in gh user (or --owner org),
  points origin at it, enables GitHub Pages via Actions.

  Refuses to push to lesley-spec template remotes.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2 ;;
    --name) REPO_NAME="$2"; shift 2 ;;
    --owner) OWNER="$2"; shift 2 ;;
    --private) VISIBILITY="private"; shift ;;
    --public) VISIBILITY="public"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ -n "$PROJECT" && -d "$PROJECT" ]] || die "--project must be an existing directory"
[[ -n "$REPO_NAME" ]] || die "--name is required (repo slug, e.g. partner-ups-step-2)"

if [[ ! "$REPO_NAME" =~ ^[A-Za-z0-9._-]+$ ]]; then
  die "Repo name must be letters, numbers, dot, underscore, or hyphen: $REPO_NAME"
fi

command -v git >/dev/null 2>&1 || die "git is required"
command -v gh >/dev/null 2>&1 || die "gh is required — re-run ensure-harness.sh"

gh auth status >/dev/null 2>&1 || die "GitHub CLI is not logged in.
Ask the designer to run: gh auth login
Then re-run publish-repo.sh."

LOGIN="$(gh api user --jq .login)"
[[ -n "$LOGIN" ]] || die "Could not read GitHub login from gh api user"
if [[ -z "$OWNER" ]]; then
  OWNER="$LOGIN"
fi

info "GitHub login: $LOGIN"
info "Repo owner:   $OWNER/$REPO_NAME ($VISIBILITY)"

if [[ "$OWNER" != "$LOGIN" ]]; then
  info "Owner differs from login — creating under org/user '$OWNER' (designer must have create-repo permission)."
fi

# Guard: never create under a hard-coded template account unless that IS the login.
TEMPLATE_ACCOUNT="lesley-spec"
if [[ "$OWNER" == "$TEMPLATE_ACCOUNT" && "$LOGIN" != "$TEMPLATE_ACCOUNT" ]]; then
  die "Refusing to create a repo under $TEMPLATE_ACCOUNT (logged in as $LOGIN).
Designers publish to their own GitHub user, or an org they can create repos in.
See ux-prototyping/references/github.md"
fi

cd "$PROJECT"
[[ -d .git ]] || die "$PROJECT is not a git repo"

is_template_url() {
  local u="${1:-}"
  [[ "$u" == *lesley-spec/one-program-1* || "$u" == *lesley-spec/PartnerUI-shell* ]]
}

if git remote get-url origin >/dev/null 2>&1; then
  ORIGIN_URL="$(git remote get-url origin)"
  if is_template_url "$ORIGIN_URL"; then
    info "Renaming template remote origin → template ($ORIGIN_URL)"
    git remote rename origin template 2>/dev/null || git remote remove origin
  elif [[ "$ORIGIN_URL" == *"github.com/${OWNER}/${REPO_NAME}"* ]]; then
    info "origin already points at $OWNER/$REPO_NAME — will push"
  else
    die "origin is already set to $ORIGIN_URL
Not overwriting. Rename/remove origin, or pass a different --name."
  fi
fi

# Vite base must match GitHub project Pages path /<repo>/
_set_vite_base() {
  local cfg=""
  for cfg in vite.config.ts vite.config.js vite.config.mts vite.config.mjs; do
    [[ -f "$cfg" ]] && break
    cfg=""
  done
  [[ -n "$cfg" ]] || return 0
  python3 - "$cfg" "$REPO_NAME" <<'PY'
import re, sys
from pathlib import Path
path, name = Path(sys.argv[1]), sys.argv[2]
text = path.read_text(encoding="utf-8")
base = f"/{name}/"
if re.search(r"\bbase\s*:", text):
    text = re.sub(r"(\bbase\s*:\s*)(['\"]).*?\2", rf"\1'{base}'", text, count=1)
else:
    text = re.sub(
        r"(defineConfig\s*\(\s*\{)",
        rf"\1\n  base: '{base}',",
        text,
        count=1,
    )
path.write_text(text, encoding="utf-8")
print(f"set {path} base to {base}")
PY
}

_set_vite_base

WF_DIR=".github/workflows"
mkdir -p "$WF_DIR"
if [[ ! -f "$WF_DIR/pages.yml" && ! -f "$WF_DIR/pages.yaml" ]]; then
  cp "$SCRIPT_DIR/pages.yml" "$WF_DIR/pages.yml"
  info "Added $WF_DIR/pages.yml"
fi

if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "Prepare ${REPO_NAME} for GitHub Pages (vite base + Pages workflow)"
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  info "Creating GitHub repo ${OWNER}/${REPO_NAME}…"
  vis_flag="--public"
  [[ "$VISIBILITY" == "private" ]] && vis_flag="--private"
  gh repo create "${OWNER}/${REPO_NAME}" $vis_flag --source=. --remote=origin --push
else
  info "Pushing to origin…"
  git push -u origin HEAD
fi

info "Enabling GitHub Pages (Actions)…"
if ! gh api "repos/${OWNER}/${REPO_NAME}/pages" >/dev/null 2>&1; then
  gh api -X POST "repos/${OWNER}/${REPO_NAME}/pages" \
    -f build_type=workflow >/dev/null || info "Pages API create returned an error — enable Pages in repo Settings if needed."
else
  gh api -X PUT "repos/${OWNER}/${REPO_NAME}/pages" \
    -f build_type=workflow >/dev/null || true
fi

REPO_URL="https://github.com/${OWNER}/${REPO_NAME}"
PAGES_URL="https://${OWNER}.github.io/${REPO_NAME}/"

cat <<EOF

═══════════════════════════════════════════════════════════
 PROTOTYPE PUBLISHED
═══════════════════════════════════════════════════════════
 GitHub user:  ${LOGIN}
 Repo:         ${REPO_URL}
 Pages:        ${PAGES_URL}
               (first deploy may take 1–2 minutes — GitHub Actions)

 Open the Pages URL after the Actions run is green.

IMPACT_PROTOTYPE_PUBLISHED repo=${REPO_URL} pages=${PAGES_URL} owner=${OWNER} login=${LOGIN}
═══════════════════════════════════════════════════════════
EOF
