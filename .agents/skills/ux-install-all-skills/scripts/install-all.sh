#!/usr/bin/env bash
# Install all 37 UX Design Thinking + UX Research pipeline skills into a project + globally.
# Usage:
#   bash install-all.sh
#   bash install-all.sh --target ~/my-project
#   bash install-all.sh --project-only
#   bash install-all.sh --global-only
#   bash install-all.sh --update
#   curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install-all.sh | bash
#   curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install-all.sh | bash -s -- --update
set -euo pipefail

ZIP_URL="${DESIGNOPS_SKILLS_ZIP:-https://lesley-spec.github.io/uxdesignops/skills/designops-skills.zip}"

PIPELINE_SKILLS=(
  design-thinking-ux
  ux-research
  assumption-mapper
  research-intake
  user-context
  user-personas
  research-planner
  research-builder
  study-summary
  competitive-analysis
  frame-maintenance
  user-research
  research-synthesis
  synthesize-research
  data-analyze
  write-spec
  anti-sycophancy
  brand-operator-ux-persona
  creator-affiliate-ux-persona
  design-system
  measurable-check
  panel-planner
  ideate
  talk-to-users
  ux-critique
  prototype-handoff
  ux-prototyping
  brand-prototype
  partner-prototype
  heuristic-evaluation
  persona-check
  test-plan
  accessibility-review
  test-loopback
  findings-publish
  ab-test-planner
  adoption-check
)

TARGET="."
DO_PROJECT=1
DO_GLOBAL=1
DO_UPDATE=0

die() { echo "ERROR: $*" >&2; exit 1; }
info() { echo "→ $*"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --project-only) DO_GLOBAL=0; shift ;;
    --global-only) DO_PROJECT=0; shift ;;
    --update) DO_UPDATE=1; shift ;;
    --no-global) DO_GLOBAL=0; shift ;;
    -h|--help)
      sed -n '2,10p' "$0"
      exit 0
      ;;
    *) die "Unknown flag: $1 (use --target PATH | --project-only | --global-only | --update)" ;;
  esac
done

[[ "$DO_PROJECT" -eq 1 || "$DO_GLOBAL" -eq 1 ]] || die "Nothing to do (both project and global disabled)."

_download() {
  local url="$1" dest="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fL --retry 3 --retry-delay 2 "$url" -o "$dest"
  else
    wget -q "$url" -O "$dest"
  fi
}

_phys() {
  (cd "$1" && pwd -P)
}

SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
if [[ -f "$SCRIPT_PATH" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd -P)"
fi

# Prefer sibling skills (this repo / an existing pack). Else download the zip.
SOURCE_PARENT=""
EXTRACT_TMP=""
if [[ -n "${SCRIPT_DIR:-}" && -f "$SCRIPT_DIR/../../design-thinking-ux/SKILL.md" ]]; then
  SOURCE_PARENT="$(_phys "$SCRIPT_DIR/../..")"
  info "Using local skills at $SOURCE_PARENT"
else
  command -v unzip >/dev/null 2>&1 || die "Need unzip to extract the skills pack."
  command -v curl >/dev/null 2>&1 || command -v wget >/dev/null 2>&1 || \
    die "Need curl or wget to download the skills pack."
  EXTRACT_TMP="$(mktemp -d)"
  info "Downloading skills pack…"
  if ! _download "$ZIP_URL" "$EXTRACT_TMP/skills.zip"; then
    rm -rf "$EXTRACT_TMP"
    die "Could not download $ZIP_URL
Re-run with network / sandbox off (Cursor: required_permissions [\"all\"])."
  fi
  mkdir -p "$EXTRACT_TMP/extract"
  unzip -q "$EXTRACT_TMP/skills.zip" -d "$EXTRACT_TMP/extract"
  SOURCE_PARENT="$EXTRACT_TMP/extract"
fi

_is_skill_dir() {
  local dir="$1"
  [[ -d "$dir" && -f "$dir/SKILL.md" ]]
}

_copy_skill() {
  local src="$1" dest="$2"
  if [[ -e "$dest" && "$(_phys "$src")" == "$(_phys "$dest")" ]]; then
    info "Already present: $(basename "$src")"
    return 0
  fi
  rm -rf "$dest"
  mkdir -p "$dest"
  tar -C "$src" \
    --exclude='.tmp-toolchain-test' \
    --exclude='__pycache__' \
    --exclude='.DS_Store' \
    -cf - . | tar -C "$dest" -xf -
}

_link_skill() {
  local name="$1" dest_dir="$2" rel="$3"
  mkdir -p "$dest_dir"
  rm -rf "$dest_dir/$name"
  ln -sfn "$rel/$name" "$dest_dir/$name"
}

# The full pack is present only when every required skill is on disk.
# A partial copy is installed again. A complete copy is left alone unless --update.
_pack_present() {
  local base="$1" name
  [[ -d "$base" ]] || return 1
  for name in "${PIPELINE_SKILLS[@]}" ux-install-all-skills; do
    [[ -f "$base/$name/SKILL.md" ]] || return 1
  done
}

# Every skill folder in the pack (37 pipeline + this installer + any extras).
ALL_NAMES=()
for skill_dir in "$SOURCE_PARENT"/*/; do
  [[ -d "$skill_dir" ]] || continue
  name="$(basename "$skill_dir")"
  _is_skill_dir "$skill_dir" || continue
  ALL_NAMES+=("$name")
done
[[ ${#ALL_NAMES[@]} -gt 0 ]] || die "No SKILL.md folders found in $SOURCE_PARENT"

for name in "${PIPELINE_SKILLS[@]}"; do
  _is_skill_dir "$SOURCE_PARENT/$name" || die "Skills pack is missing required skill: $name"
done

project_agents=""
project_state="skipped"
cursor_global="${HOME}/.cursor/skills"
claude_global="${HOME}/.claude/skills"
cursor_global_ok="no"
claude_global_ok="no"

_install_tree() {
  local dest_root="$1"
  mkdir -p "$dest_root"
  local name
  for name in "${ALL_NAMES[@]}"; do
    _copy_skill "$SOURCE_PARENT/$name" "$dest_root/$name"
  done
}

if [[ "$DO_PROJECT" -eq 1 ]]; then
  TARGET="$(cd "$TARGET" && pwd)" || die "Cannot cd to --target $TARGET"
  project_agents="$TARGET/.agents/skills"
  if [[ "$DO_UPDATE" -eq 0 ]] && _pack_present "$project_agents"; then
    info "Already installed in this project: $project_agents"
    project_state="already"
  else
    info "Installing into $project_agents (Cursor + Claude symlinks)…"
    mkdir -p "$project_agents" "$TARGET/.cursor/skills" "$TARGET/.claude/skills"
    for name in "${ALL_NAMES[@]}"; do
      _copy_skill "$SOURCE_PARENT/$name" "$project_agents/$name"
      _link_skill "$name" "$TARGET/.cursor/skills" "../../.agents/skills"
      _link_skill "$name" "$TARGET/.claude/skills" "../../.agents/skills"
    done
    project_state="installed"
  fi
fi

if [[ "$DO_GLOBAL" -eq 1 ]]; then
  if [[ "$DO_UPDATE" -eq 0 ]] && _pack_present "$cursor_global"; then
    info "Already installed for Cursor: $cursor_global"
    cursor_global_ok="already"
  else
    info "Installing globally for Cursor…"
    _install_tree "$cursor_global"
    cursor_global_ok="yes"
  fi
  if [[ "$DO_UPDATE" -eq 0 ]] && _pack_present "$claude_global"; then
    info "Already installed for Claude Code: $claude_global"
    claude_global_ok="already"
  else
    info "Installing globally for Claude Code…"
    _install_tree "$claude_global"
    claude_global_ok="yes"
  fi
fi

missing=()
_check_required() {
  local base="$1"
  local name
  for name in "${PIPELINE_SKILLS[@]}"; do
    if [[ ! -f "$base/$name/SKILL.md" ]]; then
      missing+=("$base/$name")
    fi
  done
}

if [[ "$DO_PROJECT" -eq 1 ]]; then
  _check_required "$project_agents"
fi
if [[ "$DO_GLOBAL" -eq 1 ]]; then
  _check_required "$cursor_global"
  _check_required "$claude_global"
fi
[[ ${#missing[@]} -eq 0 ]] || die "Missing SKILL.md after install:
$(printf '  %s\n' "${missing[@]}")"

[[ -n "$EXTRACT_TMP" ]] && rm -rf "$EXTRACT_TMP"

project_line="${project_agents:-skipped}"
skill_n="${#ALL_NAMES[@]}"

cat <<EOF

═══════════════════════════════════════════════════════════
 UX DESIGN THINKING SKILLS READY
═══════════════════════════════════════════════════════════
 pipeline skills:  37 / 37
 pack folders:     ${skill_n}
 project:          ${project_state}  (${project_line})
 Cursor global:    ${cursor_global_ok}  (${cursor_global})
 Claude global:    ${claude_global_ok}  (${claude_global})

 already = left in place. installed = copied now. Say "update the pack" to replace a copy.

 Next: in chat, say  use design-thinking-ux
 or  use ux-research  for research + Frame skills.

IMPACT_SKILLS_READY pipeline=37 dest=${project_line} project=${project_state} global_cursor=${cursor_global_ok} global_claude=${claude_global_ok}
═══════════════════════════════════════════════════════════
EOF
