"""Write a short catalogue of Dovetail insights and Outset studies.

Reads API keys from the environment. Prints counts and HTTP status only.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

OUT = Path(os.environ.get("CATALOGUE_OUT", "catalogue.md"))
LOOKBACK_DAYS = int(os.environ.get("LOOKBACK_DAYS", "90"))
MAX_ITEMS = int(os.environ.get("MAX_ITEMS", "40"))


def _dovetail() -> tuple[list[dict], str]:
    key = os.environ.get("DOVETAIL_API_KEY", "").strip()
    base = os.environ.get("DOVETAIL_BASE_URL", "https://dovetail.com").rstrip("/")
    if not key:
        return [], "Dovetail API key is not set."

    created_after = (datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)).strftime("%Y-%m-%d")
    items: list[dict] = []
    cursor = None
    try:
        while len(items) < MAX_ITEMS:
            params = {
                "page[limit]": min(100, MAX_ITEMS - len(items)),
                "filter[created_at][gte]": created_after,
            }
            if cursor:
                params["page[start_cursor]"] = cursor
            response = requests.get(
                f"{base}/api/v1/insights",
                headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
                params=params,
                timeout=60,
            )
            print(f"dovetail insights HTTP {response.status_code}")
            response.raise_for_status()
            payload = response.json()
            for item in payload.get("data", []):
                if item.get("deleted"):
                    continue
                title = (item.get("title") or "").strip() or "Untitled insight"
                items.append(
                    {
                        "title": title,
                        "created_at": (item.get("created_at") or "")[:10],
                        "url": item.get("url") or "",
                        "project": item.get("project_title") or "",
                    }
                )
                if len(items) >= MAX_ITEMS:
                    break
            page = payload.get("page") or {}
            if not page.get("has_more"):
                break
            cursor = page.get("next_cursor")
            if not cursor:
                break
    except requests.RequestException as exc:
        status = getattr(getattr(exc, "response", None), "status_code", "error")
        return items, f"Dovetail request failed (HTTP {status})."
    return items, ""


def _outset() -> tuple[list[dict], str]:
    key = os.environ.get("OUTSET_API_KEY", "").strip()
    base = os.environ.get("OUTSET_API_BASE_URL", "https://api.outset.ai").rstrip("/")
    if not key:
        return [], "Outset API key is not set."

    studies: list[dict] = []
    url = f"{base}/v1/studies/"
    try:
        while url and len(studies) < MAX_ITEMS:
            response = requests.get(
                url,
                headers={"Authorization": f"Api-Key {key}", "Accept": "application/json"},
                timeout=30,
            )
            print(f"outset studies HTTP {response.status_code}")
            response.raise_for_status()
            payload = response.json()
            for item in payload.get("results", []):
                name = (item.get("name") or "Untitled study").strip()
                studies.append(
                    {
                        "title": name,
                        "url": item.get("start_url") or "",
                        "active": item.get("active"),
                    }
                )
                if len(studies) >= MAX_ITEMS:
                    break
            url = payload.get("next") if len(studies) < MAX_ITEMS else None
    except requests.RequestException as exc:
        status = getattr(getattr(exc, "response", None), "status_code", "error")
        return studies, f"Outset request failed (HTTP {status})."
    return studies, ""


def _lines(items: list[dict], note: str, kind: str) -> list[str]:
    if note and not items:
        return [note, ""]
    lines = [f"{len(items)} {kind}.", ""]
    if note:
        lines = [note, ""] + lines
    for item in items:
        title = item["title"].replace("|", "/")
        url = item.get("url") or ""
        extra = item.get("created_at") or ("active" if item.get("active") else "")
        project = item.get("project") or ""
        bits = [b for b in (extra, project) if b]
        suffix = f" ({', '.join(bits)})" if bits else ""
        if url:
            lines.append(f"- [{title}]({url}){suffix}")
        else:
            lines.append(f"- {title}{suffix}")
    lines.append("")
    return lines


def main() -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    insights, dove_note = _dovetail()
    studies, outset_note = _outset()
    body = [
        f"# Research source catalogue ({today})",
        "",
        f"Lookback for Dovetail insights: {LOOKBACK_DAYS} days. Capped at {MAX_ITEMS} items per source.",
        "",
        "## Dovetail",
        "",
        *_lines(insights, dove_note, "insights"),
        "## Outset",
        "",
        *_lines(studies, outset_note, "studies"),
    ]
    OUT.write_text("\n".join(body), encoding="utf-8")
    print(f"wrote {OUT} insights={len(insights)} studies={len(studies)}")


if __name__ == "__main__":
    main()
