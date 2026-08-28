#!/usr/bin/env bash
# Install UX DesignOps agent skills into a project directory.
# Usage:
#   curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install.sh | bash -s -- cursor .
#   curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install.sh | bash -s -- claude ~/my-project
#   bash install.sh agents .

set -euo pipefail

HARNESS="${1:-agents}"
TARGET="${2:-.}"
ZIP_URL="${DESIGNOPS_SKILLS_ZIP:-https://lesley-spec.github.io/uxdesignops/skills/designops-skills.zip}"

case "$HARNESS" in
  cursor|Cursor) DEST_REL=".cursor/skills" ;;
  claude|Claude) DEST_REL=".claude/skills" ;;
  agents|copilot|codex|Agents) DEST_REL=".agents/skills" ;;
  *)
    echo "Unknown harness: $HARNESS" >&2
    echo "Use: cursor | claude | agents" >&2
    exit 1
    ;;
esac

TARGET="$(cd "$TARGET" && pwd)"
DEST="$TARGET/$DEST_REL"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "→ Downloading skills pack…"
if command -v curl >/dev/null 2>&1; then
  curl -fsSL "$ZIP_URL" -o "$TMP/skills.zip"
elif command -v wget >/dev/null 2>&1; then
  wget -qO "$TMP/skills.zip" "$ZIP_URL"
else
  echo "Need curl or wget to download the skills pack." >&2
  exit 1
fi

echo "→ Extracting to $DEST …"
mkdir -p "$DEST"
unzip -q "$TMP/skills.zip" -d "$TMP/extract"

count=0
for skill_dir in "$TMP/extract"/*/; do
  name="$(basename "$skill_dir")"
  [[ "$name" == "README.md" ]] && continue
  rm -rf "$DEST/$name"
  cp -R "$skill_dir" "$DEST/$name"
  count=$((count + 1))
done

echo "✓ Installed $count skills into $DEST ($HARNESS harness)"
echo "  Invoke in chat, e.g. use design-thinking-ux · use write-spec · use ideate · use test-plan"
