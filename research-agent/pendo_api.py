"""Fetch Pendo product analytics and in-app poll feedback via Aggregation API."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests

PENDO_API_KEY = os.environ.get("PENDO_API_KEY", "")
PENDO_SUBSCRIPTION_ID = os.environ.get("PENDO_SUBSCRIPTION_ID", "")
PENDO_REGION = os.environ.get("PENDO_REGION", "US").upper()
PENDO_APP_ID = os.environ.get("PENDO_APP_ID", "-323232")  # Impact default app
PENDO_MAX_FEEDBACK = int(os.environ.get("PENDO_MAX_FEEDBACK", "200"))
PENDO_TOP_N = int(os.environ.get("PENDO_TOP_N", "25"))

PENDO_REGION_URLS = {
    "US": "https://app.pendo.io",
    "EU": "https://app.eu.pendo.io",
    "US1": "https://us1.app.pendo.io",
    "JPN": "https://app.jpn.pendo.io",
    "AU": "https://app.au.pendo.io",
}

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


def get_pendo_base_url() -> str:
    if PENDO_REGION in PENDO_REGION_URLS:
        return PENDO_REGION_URLS[PENDO_REGION]
    if PENDO_API_KEY and "." in PENDO_API_KEY:
        suffix = PENDO_API_KEY.rsplit(".", 1)[-1].lower()
        region_map = {"us": "US", "eu": "EU", "us1": "US1", "jpn": "JPN", "au": "AU"}
        region = region_map.get(suffix)
        if region:
            return PENDO_REGION_URLS[region]
    return PENDO_REGION_URLS["US"]


def _lookback_epoch_ms(lookback_days: int) -> int:
    return int((datetime.now(timezone.utc) - timedelta(days=lookback_days)).timestamp() * 1000)


def _ms_to_iso(value: Any) -> str:
    if value is None or value == "":
        return ""
    try:
        ms = int(value)
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return str(value)


def _aggregate(pipeline: List[Dict[str, Any]], request_id: str, timeout: int = 120) -> List[Dict[str, Any]]:
    url = f"{get_pendo_base_url()}/api/v1/aggregation"
    headers = {
        "Content-Type": "application/json",
        "X-Pendo-Integration-Key": PENDO_API_KEY,
    }
    payload = {
        "response": {"mimeType": "application/json"},
        "request": {"requestId": request_id, "pipeline": pipeline},
    }
    response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        results = data.get("results")
        if isinstance(results, list):
            return results
        if results is not None:
            return [results]
    return []


def _catalog_names(kind: str) -> Dict[str, str]:
    """Map page/feature/guide id → name."""
    source_key = {"page": "pages", "feature": "features", "guide": "guides"}[kind]
    rows = _aggregate([{"source": {source_key: None}}], f"research-agent-{source_key}")
    names: Dict[str, str] = {}
    for row in rows:
        entity_id = row.get("id")
        if entity_id:
            names[str(entity_id)] = row.get("name") or str(entity_id)
    return names


def _period_end_iso() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _analytics_item(
    *,
    item_type: str,
    title: str,
    subtitle: str,
    metric: str,
    entity_id: str = "",
    events: int = 0,
    visitors: int = 0,
    rage: int = 0,
    dead: int = 0,
    detail: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "source": "pendo",
        "kind": "analytics",
        "type": item_type,
        "title": title,
        "subtitle": subtitle,
        "body": subtitle,
        "metric": metric,
        "entity_id": entity_id,
        "events": events,
        "visitors": visitors,
        "rage_clicks": rage,
        "dead_clicks": dead,
        "created_at": _period_end_iso(),
        "timestamp": _period_end_iso(),
        "search_terms": _search_terms(f"{title} {subtitle}"),
        "detail": detail or {},
    }


def _query_top_pages(lookback_days: int, page_names: Dict[str, str]) -> List[Dict[str, Any]]:
    start = _lookback_epoch_ms(lookback_days)
    rows = _aggregate(
        [
            {
                "source": {
                    "pageEvents": None,
                    "timeSeries": {"period": "dayRange", "first": start, "count": lookback_days},
                }
            },
            {
                "group": {
                    "group": ["pageId"],
                    "fields": {
                        "events": {"sum": "numEvents"},
                        "visitors": {"count": "visitorId"},
                        "rage": {"sum": "rageClickCount"},
                        "dead": {"sum": "deadClickCount"},
                    },
                }
            },
            {"sort": ["-events"]},
            {"limit": PENDO_TOP_N},
        ],
        "research-agent-top-pages",
    )
    items: List[Dict[str, Any]] = []
    for row in rows:
        page_id = str(row.get("pageId") or "")
        name = page_names.get(page_id, page_id or "Unknown page")
        events = int(row.get("events") or 0)
        visitors = int(row.get("visitors") or 0)
        rage = int(row.get("rage") or 0)
        dead = int(row.get("dead") or 0)
        items.append(
            _analytics_item(
                item_type="Page",
                title=name,
                subtitle=f"Top page by views · {visitors:,} visitors · {rage:,} rage / {dead:,} dead clicks",
                metric=f"{events:,} views",
                entity_id=page_id,
                events=events,
                visitors=visitors,
                rage=rage,
                dead=dead,
                detail=row,
            )
        )
    return items


def _query_top_features(lookback_days: int, feature_names: Dict[str, str]) -> List[Dict[str, Any]]:
    start = _lookback_epoch_ms(lookback_days)
    rows = _aggregate(
        [
            {
                "source": {
                    "featureEvents": None,
                    "timeSeries": {"period": "dayRange", "first": start, "count": lookback_days},
                }
            },
            {
                "group": {
                    "group": ["featureId"],
                    "fields": {
                        "count": {"count": None},
                        "visitors": {"count": "visitorId"},
                        "rage": {"sum": "rageClickCount"},
                        "dead": {"sum": "deadClickCount"},
                    },
                }
            },
            {"sort": ["-count"]},
            {"limit": PENDO_TOP_N},
        ],
        "research-agent-top-features",
    )
    items: List[Dict[str, Any]] = []
    for row in rows:
        feature_id = str(row.get("featureId") or "")
        name = feature_names.get(feature_id, feature_id or "Unknown feature")
        events = int(row.get("count") or 0)
        visitors = int(row.get("visitors") or 0)
        rage = int(row.get("rage") or 0)
        dead = int(row.get("dead") or 0)
        items.append(
            _analytics_item(
                item_type="Feature",
                title=name,
                subtitle=f"Top feature by clicks · {visitors:,} visitors · {rage:,} rage clicks",
                metric=f"{events:,} clicks",
                entity_id=feature_id,
                events=events,
                visitors=visitors,
                rage=rage,
                dead=dead,
                detail=row,
            )
        )
    return items


def _query_friction_pages(lookback_days: int, page_names: Dict[str, str]) -> List[Dict[str, Any]]:
    start = _lookback_epoch_ms(lookback_days)
    rows = _aggregate(
        [
            {
                "source": {
                    "pageEvents": None,
                    "timeSeries": {"period": "dayRange", "first": start, "count": lookback_days},
                }
            },
            {
                "group": {
                    "group": ["pageId"],
                    "fields": {
                        "events": {"sum": "numEvents"},
                        "visitors": {"count": "visitorId"},
                        "rage": {"sum": "rageClickCount"},
                        "dead": {"sum": "deadClickCount"},
                        "error": {"sum": "errorClickCount"},
                    },
                }
            },
            {"sort": ["-rage"]},
            {"limit": PENDO_TOP_N},
        ],
        "research-agent-friction-pages",
    )
    items: List[Dict[str, Any]] = []
    for row in rows:
        rage = int(row.get("rage") or 0)
        if rage <= 0:
            continue
        page_id = str(row.get("pageId") or "")
        name = page_names.get(page_id, page_id or "Unknown page")
        visitors = int(row.get("visitors") or 0)
        dead = int(row.get("dead") or 0)
        error = int(row.get("error") or 0)
        items.append(
            _analytics_item(
                item_type="Friction",
                title=name,
                subtitle=(
                    f"High friction page · {rage:,} rage · {dead:,} dead · "
                    f"{error:,} error clicks · {visitors:,} visitors"
                ),
                metric=f"{rage:,} rage clicks",
                entity_id=page_id,
                events=int(row.get("events") or 0),
                visitors=visitors,
                rage=rage,
                dead=dead,
                detail=row,
            )
        )
    return items


def _query_poll_feedback(lookback_days: int, guide_names: Dict[str, str]) -> List[Dict[str, Any]]:
    start = _lookback_epoch_ms(lookback_days)
    events = _aggregate(
        [
            {
                "source": {
                    "pollEvents": None,
                    "timeSeries": {"period": "dayRange", "first": start, "count": lookback_days},
                }
            }
        ],
        "research-agent-poll-events",
        timeout=180,
    )

    feedback: List[Dict[str, Any]] = []
    for event in events:
        if len(feedback) >= PENDO_MAX_FEEDBACK:
            break

        response_text = event.get("pollResponse")
        if not isinstance(response_text, str) or not response_text.strip():
            continue

        stripped = response_text.strip()
        poll_type = str(event.get("pollType") or "")
        # Keep free-text / longer answers; skip bare NPS digits unless OpenText
        if stripped.isdigit() and len(stripped) <= 2 and "Open" not in poll_type and "Text" not in poll_type:
            continue
        if len(stripped) < 4 and poll_type in {"NPSRating", "PositiveNegative", "NumberScale"}:
            continue

        guide_id = str(event.get("guideId") or "")
        guide_name = guide_names.get(guide_id, guide_id or "Unknown guide")
        timestamp = _ms_to_iso(event.get("browserTime") or event.get("receivedTime"))

        feedback.append({
            "source": "pendo",
            "kind": "feedback",
            "type": "Feedback",
            "guide_id": guide_id,
            "guide_name": guide_name,
            "title": guide_name,
            "subtitle": stripped[:180],
            "poll_id": event.get("pollId", ""),
            "poll_type": poll_type,
            "response": stripped,
            "body": stripped,
            "visitor_id": event.get("visitorId", ""),
            "timestamp": timestamp,
            "created_at": timestamp,
            "metric": poll_type or "Poll",
            "search_terms": _search_terms(f"{guide_name} {stripped}"),
        })

    return feedback


def query_pendo_items(lookback_days: int = 90) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Return (feedback_items, analytics_items) for the lookback window.

    feedback_items — open-text poll responses (for enrichment + listing)
    analytics_items — top pages, features, and friction signals
    """
    print("\n💬 Querying Pendo (product analytics + feedback)...")

    if not PENDO_API_KEY:
        print("  ⚠️  Pendo API key not set, skipping")
        return [], []

    feedback: List[Dict[str, Any]] = []
    analytics: List[Dict[str, Any]] = []

    try:
        print("  · Loading page / feature / guide catalogs...")
        page_names = _catalog_names("page")
        feature_names = _catalog_names("feature")
        guide_names = _catalog_names("guide")
        print(f"  · Catalog: {len(page_names)} pages, {len(feature_names)} features, {len(guide_names)} guides")

        analytics.extend(_query_top_pages(lookback_days, page_names))
        print(f"  · Top pages: {sum(1 for i in analytics if i['type'] == 'Page')}")

        analytics.extend(_query_top_features(lookback_days, feature_names))
        print(f"  · Top features: {sum(1 for i in analytics if i['type'] == 'Feature')}")

        analytics.extend(_query_friction_pages(lookback_days, page_names))
        print(f"  · Friction pages: {sum(1 for i in analytics if i['type'] == 'Friction')}")

        feedback = _query_poll_feedback(lookback_days, guide_names)
        print(f"  · Poll feedback: {len(feedback)}")

        print(
            f"  ✅ Pendo: {len(analytics)} analytics + {len(feedback)} feedback "
            f"(last {lookback_days} days)"
        )
    except Exception as exc:
        print(f"  ⚠️  Pendo query failed: {exc}")

    return feedback, analytics


def query_pendo_feedback(lookback_days: int = 90) -> List[Dict[str, Any]]:
    """Backward-compatible helper — feedback only."""
    feedback, _ = query_pendo_items(lookback_days=lookback_days)
    return feedback
