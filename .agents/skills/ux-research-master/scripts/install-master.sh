#!/usr/bin/env bash
# One front door: install every UX skill, the /ux-* commands, and the routing
# rule block.
#
# Usage:
#   bash install-master.sh
#   bash install-master.sh --target ~/my-project
#   bash install-master.sh --project-only | --global-only
#   bash install-master.sh --no-rules | --no-commands
#   curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install-all.sh | bash
set -euo pipefail

PAGES_BASE="${DESIGNOPS_PAGES_BASE:-https://lesley-spec.github.io/uxdesignops/skills}"

TARGET="."
DO_PROJECT=1
DO_GLOBAL=1
DO_RULES=1
DO_COMMANDS=1
DO_SKILLS=1

die() { echo "ERROR: $*" >&2; exit 1; }
info() { echo "→ $*"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --project-only) DO_GLOBAL=0; shift ;;
    --global-only) DO_PROJECT=0; DO_RULES=0; shift ;;
    --no-global) DO_GLOBAL=0; shift ;;
    --no-rules) DO_RULES=0; shift ;;
    --no-commands) DO_COMMANDS=0; shift ;;
    --skip-skills) DO_SKILLS=0; shift ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) die "Unknown flag: $1" ;;
  esac
done

[[ "$DO_PROJECT" -eq 1 || "$DO_GLOBAL" -eq 1 ]] || die "Nothing to do."

SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
SCRIPT_DIR=""
[[ -f "$SCRIPT_PATH" ]] && SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd -P)"
SKILL_DIR="${SCRIPT_DIR:+$(cd "$SCRIPT_DIR/.." && pwd -P)}"

# ── 1. Skills ───────────────────────────────────────────────────────────────
INSTALL_ALL=""
if [[ -n "$SKILL_DIR" && -f "$SKILL_DIR/../ux-install-all-skills/scripts/install-all.sh" ]]; then
  INSTALL_ALL="$(cd "$SKILL_DIR/../ux-install-all-skills/scripts" && pwd -P)/install-all.sh"
fi

all_args=()
[[ "$DO_PROJECT" -eq 0 ]] && all_args+=(--global-only)
[[ "$DO_GLOBAL" -eq 0 ]] && all_args+=(--project-only)
[[ "$DO_PROJECT" -eq 1 ]] && all_args+=(--target "$TARGET")

if [[ "$DO_SKILLS" -eq 1 ]]; then
  export UX_SKIP_POST=1   # install-all.sh must not call us back
  if [[ -n "$INSTALL_ALL" ]]; then
    info "Installing skills via $INSTALL_ALL"
    bash "$INSTALL_ALL" "${all_args[@]}"
  else
    info "No local pack — bootstrapping from $PAGES_BASE"
    command -v curl >/dev/null 2>&1 || die "Need curl to bootstrap the pack."
    curl -fsSL "$PAGES_BASE/install-all.sh" | bash -s -- "${all_args[@]}"
  fi
  unset UX_SKIP_POST
else
  info "Skills already installed — commands and rules only"
fi

# Where the pack landed — prefer the project copy, fall back to the global one.
if [[ "$DO_PROJECT" -eq 1 ]]; then
  TARGET="$(cd "$TARGET" && pwd -P)"
  PACK="$TARGET/.agents/skills"
else
  PACK="$HOME/.claude/skills"
fi
MASTER="$PACK/ux-research-master"
[[ -d "$MASTER" ]] || MASTER="${SKILL_DIR:-}"
[[ -n "$MASTER" && -f "$MASTER/SKILL.md" ]] || die "ux-research-master not found after install."

# ── 2. Commands ─────────────────────────────────────────────────────────────
cmd_count=0
cmd_dests=()
if [[ "$DO_COMMANDS" -eq 1 ]]; then
  src_cmds="$MASTER/commands"
  [[ -d "$src_cmds" ]] || die "Missing $src_cmds"
  [[ "$DO_PROJECT" -eq 1 ]] && cmd_dests+=("$TARGET/.claude/commands" "$TARGET/.cursor/commands")
  [[ "$DO_GLOBAL" -eq 1 ]] && cmd_dests+=("$HOME/.claude/commands" "$HOME/.cursor/commands")
  for dest in "${cmd_dests[@]}"; do
    mkdir -p "$dest"
    for f in "$src_cmds"/*.md; do
      [[ -e "$f" ]] || continue
      cp -f "$f" "$dest/$(basename "$f")"
    done
  done
  cmd_count="$(find "$src_cmds" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')"
  info "Installed $cmd_count /ux-* commands into ${#cmd_dests[@]} locations"
fi

# ── 3. Routing rules ────────────────────────────────────────────────────────
rules_written="no"
_write_rules() {
  local file="$1" block="$2" tmp
  tmp="$(mktemp)"
  if [[ -f "$file" ]] && grep -q '<!-- BEGIN ux-research-master' "$file"; then
    awk -v blockfile="$block" '
      /<!-- BEGIN ux-research-master/ { skip=1; while ((getline line < blockfile) > 0) print line; close(blockfile) }
      /<!-- END ux-research-master/ { skip=0; next }
      !skip { print }
    ' "$file" > "$tmp"
  else
    [[ -f "$file" ]] && { cat "$file" > "$tmp"; printf '\n' >> "$tmp"; }
    cat "$block" >> "$tmp"
  fi
  mv "$tmp" "$file"
}

if [[ "$DO_RULES" -eq 1 && "$DO_PROJECT" -eq 1 ]]; then
  block="$MASTER/references/rules-block.md"
  if [[ -f "$block" ]]; then
    for f in "$TARGET/CLAUDE.md" "$TARGET/AGENTS.md"; do
      _write_rules "$f" "$block"
      info "Routing block written to $f"
    done
    rules_written="yes"
  else
    info "No rules-block.md found — skipping rule files"
  fi
fi

# ── 4. Report ───────────────────────────────────────────────────────────────
skill_n="$(find "$PACK" -maxdepth 2 -name SKILL.md 2>/dev/null | wc -l | tr -d ' ')"
project_line="no"
[[ "$DO_PROJECT" -eq 1 ]] && project_line="$TARGET"

cat <<EOF

═══════════════════════════════════════════════════════════
 UX PACK READY
═══════════════════════════════════════════════════════════
 skills:     ${skill_n}
 commands:   ${cmd_count}  (${#cmd_dests[@]} locations)
 rules:      ${rules_written}
 project:    ${project_line}
 global:     $([[ "$DO_GLOBAL" -eq 1 ]] && echo "yes (~/.claude, ~/.cursor)" || echo "no")

 Next: type  /ux   for the starter menu — or just say what you're
 working on and the right skill loads itself.

UX_MASTER_READY skills=${skill_n} commands=${cmd_count} rules=${rules_written} project=${project_line}
═══════════════════════════════════════════════════════════
EOF
