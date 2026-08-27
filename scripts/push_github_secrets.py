#!/usr/bin/env python3
"""Push secrets and variables from research-agent/.env to GitHub Actions."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / "research-agent" / ".env"

SECRET_KEYS = [
    "POSTHOG_PROJECT_ID",
    "POSTHOG_API_KEY",
    "GOOGLE_API_KEY",
    "CONFLUENCE_URL",
    "CONFLUENCE_USERNAME",
    "CONFLUENCE_API_TOKEN",
    "CONFLUENCE_SPACE",
    "DOVETAIL_API_KEY",
    "DOVETAIL_BASE_URL",
    "PENDO_API_KEY",
    "PENDO_SUBSCRIPTION_ID",
    "PENDO_REGION",
    "OUTSET_API_KEY",
    "SLACK_WEBHOOK_URL",
    "GCP_SA_KEY",
]

VAR_DEFAULTS = {
    "BIGQUERY_PROJECT": "bt-impact-labs",
    "BIGQUERY_DATASET": "prod-data-enablement",
    "BIGQUERY_TICKETS_TABLE": "datalake_freshdesk",
    "FRESHDESK_DOMAIN": "",
}


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    if not ENV_FILE.exists():
        return values
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        values[key.strip()] = val.strip()
    return values


def is_placeholder(value: str) -> bool:
    lowered = value.lower()
    return not value or "your_" in lowered or lowered.endswith("_here")


def gh(*args: str, input_text: str | None = None) -> None:
    cmd = ["gh", *args]
    subprocess.run(cmd, input=input_text, text=True, check=True)


def main() -> int:
    repo = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REPO", "impactinc/ux-designops-ai")

    try:
        subprocess.run(["gh", "auth", "status"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Run: gh auth login")
        return 1

    env = load_env()
    print(f"Syncing secrets to {repo} ...")

    for key in SECRET_KEYS:
        val = env.get(key, "")
        if is_placeholder(val):
            print(f"  skip {key}")
            continue
        gh("secret", "set", key, "--repo", repo, input_text=val)
        print(f"  ✓ {key}")

    for key, default in VAR_DEFAULTS.items():
        val = env.get(key, default)
        if not val:
            continue
        gh("variable", "set", key, "--repo", repo, "--body", val)
        print(f"  ✓ var {key}")

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
