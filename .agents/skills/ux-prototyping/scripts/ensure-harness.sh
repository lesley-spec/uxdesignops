#!/usr/bin/env bash
# ux-prototyping — verify designer harness, install missing skills + Node + gh.
# Does not start Vite (brand-prototype / partner-prototype bootstrap does that).
# Does not require gh auth.
set -euo pipefail

SKILLS_ZIP_URL="${DESIGNOPS_SKILLS_ZIP:-https://lesley-spec.github.io/uxdesignops/skills/designops-skills.zip}"
PARENT="${IMPACT_PROTOTYPE_HOME:-$HOME/Documents/impact-prototypes}"
IMPACT_GH_VERSION="${IMPACT_GH_VERSION:-2.74.0}"
NEEDED_SKILLS=(brand-prototype partner-prototype)

die() { echo "ERROR: $*" >&2; exit 1; }
info() { echo "→ $*"; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "Missing required command: $1
Install Xcode Command Line Tools (macOS: xcode-select --install), then re-run: use ux-prototyping"
}

need_cmd git
command -v curl >/dev/null 2>&1 || command -v wget >/dev/null 2>&1 || \
  die "Need curl or wget to download Node, skills, and GitHub CLI."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_PARENT="$(cd "$SKILL_ROOT/.." && pwd)"

_download() {
  local url="$1" dest="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fL --retry 3 --retry-delay 2 "${url}" -o "${dest}"
  else
    wget -q "${url}" -O "${dest}"
  fi
}

_find_skill() {
  local name="$1"
  local cand
  for cand in \
    "$SKILLS_PARENT/$name" \
    "$SKILL_ROOT/../$name" \
    "$SKILLS_PARENT/../.agents/skills/$name" \
    "$SKILLS_PARENT/../.claude/skills/$name" \
    "$SKILLS_PARENT/../.cursor/skills/$name"
  do
    if [[ -f "$cand/scripts/bootstrap.sh" && -f "$cand/SKILL.md" ]]; then
      echo "$(cd "$cand" && pwd)"
      return 0
    fi
  done
  return 1
}

_install_skills_from_zip() {
  local tmp extract name dest
  tmp="$(mktemp -d)"
  info "Downloading skills pack to install brand-prototype + partner-prototype…"
  if ! _download "$SKILLS_ZIP_URL" "$tmp/skills.zip"; then
    rm -rf "$tmp"
    die "Could not download $SKILLS_ZIP_URL
Re-run with network / sandbox off (Cursor: required_permissions [\"all\"])."
  fi
  mkdir -p "$tmp/extract"
  unzip -q "$tmp/skills.zip" -d "$tmp/extract"
  for name in "${NEEDED_SKILLS[@]}"; do
    dest="$SKILLS_PARENT/$name"
    if [[ -d "$tmp/extract/$name" ]]; then
      rm -rf "$dest"
      cp -R "$tmp/extract/$name" "$dest"
      info "Installed $name → $dest"
    else
      rm -rf "$tmp"
      die "Skills zip did not contain $name"
    fi
  done
  rm -rf "$tmp"
}

# --- sibling skills ---
missing=()
for name in "${NEEDED_SKILLS[@]}"; do
  if ! _find_skill "$name" >/dev/null; then
    missing+=("$name")
  fi
done
if [[ ${#missing[@]} -gt 0 ]]; then
  mkdir -p "$SKILLS_PARENT"
  _install_skills_from_zip
fi

BRAND_SKILL="$(_find_skill brand-prototype)" || die "brand-prototype still missing after install"
PARTNER_SKILL="$(_find_skill partner-prototype)" || die "partner-prototype still missing after install"

# --- Node (reuse Brand toolchain helper) ---
# shellcheck source=../../brand-prototype/scripts/ensure-toolchain.sh
. "$BRAND_SKILL/scripts/ensure-toolchain.sh"
impact_ensure_node

# --- GitHub CLI (local copy, no sudo; auth is a later step) ---
impact_ensure_gh() {
  if command -v gh >/dev/null 2>&1; then
    info "Using gh ($(command -v gh))"
    return 0
  fi
  info "GitHub CLI not on PATH — installing a local copy (no sudo)…"
  local os arch plat asset ext
  os="$(uname -s)"
  arch="$(uname -m)"
  case "${os}-${arch}" in
    Darwin-arm64) plat="macOS_arm64"; asset="gh_${IMPACT_GH_VERSION}_macOS_arm64.zip"; ext="zip" ;;
    Darwin-x86_64) plat="macOS_amd64"; asset="gh_${IMPACT_GH_VERSION}_macOS_amd64.zip"; ext="zip" ;;
    Linux-x86_64) plat="linux_amd64"; asset="gh_${IMPACT_GH_VERSION}_linux_amd64.tar.gz"; ext="tgz" ;;
    Linux-aarch64|Linux-arm64) plat="linux_arm64"; asset="gh_${IMPACT_GH_VERSION}_linux_arm64.tar.gz"; ext="tgz" ;;
    *) die "Cannot auto-install gh on $(uname -s) $(uname -m). Install from https://cli.github.com then re-run." ;;
  esac
  local dest="${PARENT}/.toolchain/gh-${IMPACT_GH_VERSION}"
  mkdir -p "${PARENT}/.toolchain"
  if [[ ! -x "${dest}/bin/gh" ]]; then
    local url="https://github.com/cli/cli/releases/download/v${IMPACT_GH_VERSION}/${asset}"
    local tmp
    tmp="$(mktemp -d)"
    info "Downloading ${url}"
    if ! _download "$url" "$tmp/gh.dl"; then
      rm -rf "$tmp"
      die "Failed to download GitHub CLI. Install from https://cli.github.com then re-run."
    fi
    mkdir -p "$dest/bin"
    if [[ "$ext" == "zip" ]]; then
      unzip -q "$tmp/gh.dl" -d "$tmp/out"
    else
      mkdir -p "$tmp/out"
      tar -xzf "$tmp/gh.dl" -C "$tmp/out"
    fi
    local found
    found="$(find "$tmp/out" -type f -name gh | head -1)"
    [[ -n "${found:-}" ]] || die "gh binary missing from GitHub CLI archive"
    mv "$found" "$dest/bin/gh"
    chmod +x "$dest/bin/gh"
    rm -rf "$tmp"
  fi
  export PATH="${dest}/bin:${PATH}"
  command -v gh >/dev/null 2>&1 || die "Local gh at ${dest} did not work. Install from https://cli.github.com then re-run."
  info "Provisioned gh at ${dest}"
}

impact_ensure_gh

GH_AUTH="no"
if gh auth status >/dev/null 2>&1; then
  GH_AUTH="yes"
fi

mkdir -p "$PARENT"

GH_LINE="$(gh --version 2>/dev/null || true)"
GH_LINE="${GH_LINE%%$'\n'*}"
GH_NUM="${GH_LINE#gh version }"
GH_NUM="${GH_NUM%% *}"
GIT_LINE="$(git --version)"

cat <<EOF

═══════════════════════════════════════════════════════════
 UX PROTOTYPING HARNESS READY
═══════════════════════════════════════════════════════════
 git:              ${GIT_LINE}
 Node:             $(node -v)  ($(command -v node))
 npm:              $(npm -v)
 gh:               ${GH_LINE}
 gh auth:          ${GH_AUTH}  (needed only to push a repo)
 brand-prototype:  ${BRAND_SKILL}
 partner-prototype:${PARTNER_SKILL}
 parent folder:    ${PARENT}

 Next: run brand-prototype or partner-prototype bootstrap.sh
 (sandbox off), then open the printed localhost URL.

IMPACT_HARNESS_READY git=ok node=$(node -v) npm=$(npm -v) gh=${GH_NUM} gh_auth=${GH_AUTH} brand=${BRAND_SKILL} partner=${PARTNER_SKILL}
═══════════════════════════════════════════════════════════
EOF
