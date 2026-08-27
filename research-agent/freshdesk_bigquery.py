"""Fetch recent Freshdesk support tickets from BigQuery (Freshworks datalake)."""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

BIGQUERY_PROJECT = os.environ.get("BIGQUERY_PROJECT", "bt-impact-labs")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "prod-data-enablement")
BIGQUERY_TICKETS_TABLE = os.environ.get("BIGQUERY_TICKETS_TABLE", "datalake_freshdesk")
BIGQUERY_FRESHDESK_TABLE = os.environ.get("BIGQUERY_FRESHDESK_TABLE", "")
BIGQUERY_LOOKBACK_DAYS = int(
    os.environ.get("BIGQUERY_LOOKBACK_DAYS", os.environ.get("REPORT_LOOKBACK_DAYS", "90"))
)
BIGQUERY_MAX_TICKETS = int(os.environ.get("BIGQUERY_MAX_TICKETS", "100"))


def _table_ref() -> str:
    if BIGQUERY_FRESHDESK_TABLE.strip():
        return BIGQUERY_FRESHDESK_TABLE.strip()
    return f"`{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.{BIGQUERY_TICKETS_TABLE}`"


def _build_query() -> str:
    table = _table_ref()
    return f"""
SELECT
  COALESCE(CAST(id AS STRING), CAST(ticket_id AS STRING)) AS ticket_id,
  subject,
  COALESCE(description_text, description, body, '') AS body,
  COALESCE(type, ticket_type, '') AS ticket_type,
  COALESCE(status, '') AS status,
  COALESCE(priority, '') AS priority,
  tags,
  COALESCE(group_name, CAST(group_id AS STRING), '') AS group_name,
  COALESCE(product_name, CAST(product_id AS STRING), '') AS product_name,
  created_at,
  updated_at
FROM {table}
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {BIGQUERY_LOOKBACK_DAYS} DAY)
  AND subject IS NOT NULL
ORDER BY created_at DESC
LIMIT {BIGQUERY_MAX_TICKETS}
"""


def discover_tables() -> List[str]:
    """List tables in the configured dataset (requires BigQuery credentials)."""
    from google.cloud import bigquery

    client = bigquery.Client(project=BIGQUERY_PROJECT)
    tables = client.list_tables(f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}")
    return [table.table_id for table in tables]


def query_freshdesk_tickets() -> List[Dict[str, Any]]:
    """Query recent Freshdesk tickets from BigQuery."""
    if os.environ.get("BIGQUERY_ENABLED", "true").lower() in {"0", "false", "no"}:
        print("  ℹ️  BigQuery disabled (BIGQUERY_ENABLED=false)")
        return []

    try:
        from google.cloud import bigquery
    except ImportError:
        print("  ⚠️  google-cloud-bigquery not installed, skipping Freshdesk")
        return []

    print("\n🎫 Querying Freshdesk tickets from BigQuery...")

    try:
        client = bigquery.Client(project=BIGQUERY_PROJECT)
        query = _build_query()
        rows = client.query(query).result()

        tickets: List[Dict[str, Any]] = []
        for row in rows:
            subject = (row.get("subject") or "").strip()
            body = (row.get("body") or "").strip()
            if not subject and not body:
                continue

            tags = row.get("tags")
            if isinstance(tags, str):
                try:
                    tags = json.loads(tags)
                except json.JSONDecodeError:
                    tags = [tags]
            if tags is None:
                tags = []

            created_at = row.get("created_at")
            if hasattr(created_at, "isoformat"):
                created_at = created_at.isoformat()

            ticket = {
                "source": "freshdesk",
                "ticket_id": row.get("ticket_id", ""),
                "subject": subject,
                "body": body[:2000],
                "ticket_type": str(row.get("ticket_type") or ""),
                "status": str(row.get("status") or ""),
                "priority": str(row.get("priority") or ""),
                "tags": tags if isinstance(tags, list) else [],
                "group_name": str(row.get("group_name") or ""),
                "product_name": str(row.get("product_name") or ""),
                "created_at": created_at,
                "search_terms": _extract_terms(subject, body, tags),
                "url": _freshdesk_console_url(row.get("ticket_id")),
            }
            tickets.append(ticket)

        print(f"  ✅ Found {len(tickets)} Freshdesk tickets (last {BIGQUERY_LOOKBACK_DAYS} days)")
        return tickets

    except Exception as exc:
        print(f"  ⚠️  BigQuery Freshdesk query failed: {exc}")
        print(f"  ℹ️  Table: {_table_ref()}")
        print("  ℹ️  Set BIGQUERY_FRESHDESK_TABLE if your table path differs")
        return []


def _freshdesk_console_url(ticket_id: Optional[str]) -> str:
    domain = os.environ.get("FRESHDESK_DOMAIN", "")
    if domain and ticket_id:
        return f"https://{domain}.freshdesk.com/a/tickets/{ticket_id}"
    return ""


def _extract_terms(subject: str, body: str, tags: Any) -> List[str]:
    stopwords = {
        "the", "and", "for", "with", "from", "this", "that", "have", "has", "was", "are",
        "not", "but", "can", "you", "your", "our", "ticket", "issue", "help", "please",
    }
    text = f"{subject} {body}"
    if isinstance(tags, list):
        text += " " + " ".join(str(tag) for tag in tags)

    terms = []
    for part in text.replace("/", " ").replace("-", " ").replace("_", " ").split():
        word = part.strip().lower()
        if len(word) >= 3 and word not in stopwords:
            terms.append(word)
    return list(dict.fromkeys(terms))
