#!/usr/bin/env python3
"""Validate Research Insight Agent configuration and print next steps."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"


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
    return (
        not value
        or "your_" in lowered
        or lowered.endswith("_here")
        or lowered == "changeme"
    )


def main() -> int:
    env = load_env()
    issues: list[str] = []
    ok: list[str] = []

    checks = [
        ("POSTHOG_API_KEY", True, "PostHog → Settings → Personal API keys"),
        ("GOOGLE_API_KEY", True, "Google AI Studio → API key (Gemini synthesis)"),
        ("CONFLUENCE_URL", False, "https://impact.atlassian.net/wiki"),
        ("CONFLUENCE_USERNAME", False, "your @impact.com email"),
        ("CONFLUENCE_API_TOKEN", False, "Atlassian → Security → API tokens"),
        ("DOVETAIL_API_KEY", False, "Dovetail → Account → Personal API keys"),
        ("PENDO_API_KEY", False, "Pendo → Settings → Integration keys"),
    ]

    print("Research Insight Agent — setup check\n")

    for key, required, hint in checks:
        val = env.get(key, os.environ.get(key, ""))
        if is_placeholder(val):
            label = "MISSING" if required else "optional missing"
            issues.append(f"  [{label}] {key} — {hint}")
        else:
            ok.append(f"  [ok] {key}")

    bq_project = env.get("BIGQUERY_PROJECT", "bt-impact-labs")
    ok.append(f"  [ok] BIGQUERY_PROJECT={bq_project}")

    for line in ok:
        print(line)

    if issues:
        print("\nTo fix:")
        for line in issues:
            print(line)
        print(f"\nEdit: {ENV_FILE}")

    publish_pages = env.get("PUBLISH_GITHUB_PAGES", "true").lower() not in {"0", "false", "no"}
    pages_url = env.get("GITHUB_PAGES_URL", "")
    print("\nPublishing:")
    print(f"  GitHub Pages: {'enabled' if publish_pages else 'disabled'}")
    if pages_url and not is_placeholder(pages_url):
        print(f"  Report URL: {pages_url}")
    else:
        print("  Report URL: set GITHUB_PAGES_URL after GitHub repo is created")

    print("\nBigQuery / Freshdesk:")
    print("  Local: run `gcloud auth application-default login` (needs Python 3.10+ for gcloud)")
    print("  CI: add GCP_SA_KEY secret with service account JSON")
    print("  Table: bt-impact-labs.prod-data-enablement.datalake_freshdesk")

    print("\nGitHub:")
    if Path(ROOT.parent / ".git").exists():
        print("  [ok] git initialized")
    else:
        issues.append("  [MISSING] git not initialized — run: git init -b main")
        print("  [ ] git not initialized")

    if issues:
        print(f"\n{len(issues)} item(s) need attention before a full run.")
        return 1

    print("\nAll required keys look configured. Run:")
    print("  cd research-agent && python agent_cloud.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
