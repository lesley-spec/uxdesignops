"""Fetch Outset studies via the Outset v1 REST API (Api-Key auth)."""

from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional

import requests

OUTSET_API_KEY = os.environ.get("OUTSET_API_KEY", "")
OUTSET_API_BASE_URL = os.environ.get("OUTSET_API_BASE_URL", "https://api.outset.ai").rstrip("/")
OUTSET_MAX_STUDIES = int(os.environ.get("OUTSET_MAX_STUDIES", "100"))

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


def _strip_markdown(text: str) -> str:
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text or "").strip()


def _auth_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Api-Key {OUTSET_API_KEY}",
        "Accept": "application/json",
    }


def query_outset_studies() -> List[Dict[str, Any]]:
    """List studies from Outset's v1 API."""
    if not OUTSET_API_KEY:
        print("  ⚠️  Outset API key not set, skipping")
        return []

    print("\n🎙️  Querying Outset studies via REST API...")

    studies: List[Dict[str, Any]] = []
    url: Optional[str] = f"{OUTSET_API_BASE_URL}/v1/studies/"

    try:
        while url and len(studies) < OUTSET_MAX_STUDIES:
            response = requests.get(url, headers=_auth_headers(), timeout=30)
            response.raise_for_status()
            data = response.json()

            for item in data.get("results", []):
                if len(studies) >= OUTSET_MAX_STUDIES:
                    break

                name = (item.get("name") or "Untitled study").strip()
                welcome = _strip_markdown(item.get("welcome_message") or "")
                context = _strip_markdown(item.get("context") or "")
                summary = welcome or context

                studies.append({
                    "source": "outset",
                    "id": item.get("id", ""),
                    "title": name,
                    "summary": summary[:500],
                    "body": summary[:500],
                    "url": item.get("start_url") or "",
                    "active": item.get("active"),
                    "interview_method": item.get("interview_method"),
                    "language_code": item.get("language_code"),
                    "search_terms": _search_terms(f"{name} {welcome} {context}"),
                })

            url = data.get("next") if len(studies) < OUTSET_MAX_STUDIES else None

        print(f"  ✅ Found {len(studies)} Outset studies")
        return studies

    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        print(f"  ⚠️  Outset API error ({status})")
        return studies
    except Exception as exc:
        print(f"  ⚠️  Outset query failed: {exc}")
        return studies
