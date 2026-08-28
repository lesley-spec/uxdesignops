#!/usr/bin/env python3
"""Write auth-config.js for GitHub Pages Google sign-in gate."""

from __future__ import annotations

import json
import os
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs" / "research" / "shared" / "auth-config.js"


def main() -> None:
    config = {
        "googleClientId": os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "").strip(),
        "allowedEmailDomain": os.environ.get("DESIGNOPS_AUTH_DOMAIN", "impact.com").strip()
        or "impact.com",
        "sessionHours": 24,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        f"window.DESIGNOPS_AUTH = {json.dumps(config, indent=2)};\n",
        encoding="utf-8",
    )
    print(f"  ✅ Auth config: {OUT}")


if __name__ == "__main__":
    main()
