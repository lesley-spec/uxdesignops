#!/usr/bin/env bash
# Copy .figma/make config so Figma Make can install deps and start Vite.
set -euo pipefail

SHELL_NAME=""
PROJECT=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  echo "Usage: write-figma-make-config.sh --shell brand|partner --project DIR"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --shell) SHELL_NAME="$2"; shift 2 ;;
    --project) PROJECT="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ "$SHELL_NAME" == "brand" || "$SHELL_NAME" == "partner" ]] || {
  echo "ERROR: --shell must be brand or partner" >&2
  exit 2
}
[[ -n "$PROJECT" && -d "$PROJECT" ]] || {
  echo "ERROR: --project must be an existing directory" >&2
  exit 2
}

SRC="$SCRIPT_DIR/figma-make/$SHELL_NAME"
DEST="$PROJECT/.figma/make"
mkdir -p "$DEST"
cp -R "$SRC/." "$DEST"
chmod +x "$DEST/setup" "$DEST/install" "$DEST/dev" "$DEST/verify" 2>/dev/null || true
echo "→ Wrote $DEST (shell=$SHELL_NAME)"
