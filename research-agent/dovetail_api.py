"""Fetch Dovetail insights, highlights, and notes via the v1 REST API."""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests

DOVETAIL_API_KEY = os.environ.get("DOVETAIL_API_KEY", "") or os.environ.get("DOVETAIL_API_TOKEN", "")
DOVETAIL_BASE_URL = os.environ.get("DOVETAIL_BASE_URL", "https://dovetail.com").rstrip("/")
DOVETAIL_PAGE_SIZE = int(os.environ.get("DOVETAIL_PAGE_SIZE", "100"))

STOPWORDS = {
    "flow", "the", "and", "for", "with", "from", "step", "drop", "off", "to", "a", "an",
}


def _search_terms(text: str) -> List[str]:
    tokens: List[str] = []
    for part in text.replace("/", " ").replace("-", " ").replace("_", " ").split():
        word = part.strip().lower()
        if len(word) >= 3 and word not in STOPWORDS:
            tokens.append(word)
    return tokens


def _auth_headers() -> Dict[str, str]:
    return {"Authorization": f"Bearer {DOVETAIL_API_KEY}", "Accept": "application/json"}


def _paginate_v1(endpoint: str, *, created_after: str) -> List[Dict[str, Any]]:
    """Fetch all pages from a Dovetail v1 list endpoint."""
    items: List[Dict[str, Any]] = []
    cursor: Optional[str] = None

    while True:
        params: Dict[str, Any] = {
            "page[limit]": DOVETAIL_PAGE_SIZE,
            "filter[created_at][gte]": created_after,
        }
        if cursor:
            params["page[start_cursor]"] = cursor

        response = requests.get(
            f"{DOVETAIL_BASE_URL}{endpoint}",
            headers=_auth_headers(),
            params=params,
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()

        batch = payload.get("data", [])
        items.extend(batch)

        page = payload.get("page", {})
        if not page.get("has_more"):
            break
        cursor = page.get("next_cursor")
        if not cursor:
            break

    return items


def _normalize_item(item: Dict[str, Any], item_type: str) -> Dict[str, Any]:
    title = (item.get("title") or "").strip()
    body = (item.get("text") or item.get("preview_text") or "").strip()

    if not title and body:
        title = body[:120] + ("…" if len(body) > 120 else "")
    if not title:
        title = f"Untitled {item_type}"

    return {
        "source": "dovetail",
        "type": item_type,
        "id": item.get("id", ""),
        "title": title,
        "body": body[:500],
        "preview": body[:500],
        "url": item.get("url", ""),
        "project_title": item.get("project_title") or "",
        "created_at": item.get("created_at", ""),
        "search_terms": _search_terms(f"{title} {body}"),
    }


def query_dovetail_items(lookback_days: int = 90) -> List[Dict[str, Any]]:
    """List all Dovetail insights, highlights, and notes from the lookback window."""
    if not DOVETAIL_API_KEY:
        print("  ⚠️  Dovetail API key not set, skipping")
        return []

    print("\n📚 Querying Dovetail (insights, highlights, notes)...")

    created_after = (datetime.utcnow() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    endpoints = (
        ("/api/v1/insights", "insight"),
        ("/api/v1/highlights", "highlight"),
        ("/api/v1/notes", "note"),
    )

    results: List[Dict[str, Any]] = []
    counts: Dict[str, int] = {}

    try:
        for path, item_type in endpoints:
            raw = _paginate_v1(path, created_after=created_after)
            normalized = [_normalize_item(item, item_type) for item in raw if not item.get("deleted")]
            counts[item_type] = len(normalized)
            results.extend(normalized)
            print(f"  · {item_type.capitalize()}s: {len(normalized)}")

        results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        print(f"  ✅ Found {len(results)} Dovetail items (last {lookback_days} days)")

    except Exception as exc:
        print(f"  ⚠️  Dovetail fetch failed: {exc}")

    return results
