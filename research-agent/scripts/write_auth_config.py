#!/usr/bin/env python3
"""Write auth-config.js for GitHub Pages Google sign-in gate."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs" / "research" / "shared" / "auth-config.js"


def _read_existing_client_id() -> str:
    if not OUT.is_file():
        return ""
    text = OUT.read_text(encoding="utf-8")
    match = re.search(r'"googleClientId"\s*:\s*"([^"]*)"', text)
    if match:
        return match.group(1).strip()
    match = re.search(r'googleClientId:\s*"([^"]*)"', text)
    return match.group(1).strip() if match else ""


def main() -> None:
    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "").strip()
    if not client_id:
        client_id = _read_existing_client_id()
    config = {
        "googleClientId": client_id,
        "allowedEmailDomain": os.environ.get("DESIGNOPS_AUTH_DOMAIN", "impact.com").strip()
        or "impact.com",
        "sessionHours": 24,
        "workflowAdminEmails": [
            email.strip().lower()
            for email in os.environ.get(
                "DESIGNOPS_WORKFLOW_ADMIN_EMAILS", "lesley@impact.com"
            ).split(",")
            if email.strip()
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        f"window.DESIGNOPS_AUTH = {json.dumps(config, indent=2)};\n",
        encoding="utf-8",
    )
    print(f"  ✅ Auth config: {OUT}")


if __name__ == "__main__":
    main()
