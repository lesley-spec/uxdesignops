#!/usr/bin/env python3
"""Discover Freshdesk BigQuery tables and columns. Requires gcloud ADC auth."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from freshdesk_bigquery import BIGQUERY_DATASET, BIGQUERY_PROJECT, _table_ref, discover_tables

if __name__ == "__main__":
    print(f"Project: {BIGQUERY_PROJECT}")
    print(f"Dataset: {BIGQUERY_DATASET}")
    print(f"Table: {_table_ref()}\n")
    try:
        tables = discover_tables()
        if not tables:
            print("No tables found (check dataset name and permissions)")
        else:
            print("Tables:")
            for name in tables:
                print(f"  - {name}")
    except Exception as exc:
        print(f"Error: {exc}")
        print("\nIf you can open the table in BigQuery console but get NotFound here,")
        print("your account needs BigQuery Data Viewer on prod-data-enablement.")
        print("Ask Data Platform to grant access to lesley@impact.com")
        print("\nFix auth:")
        print("  ./scripts/setup_bigquery_local.sh")
        print("  export CLOUDSDK_PYTHON=/opt/homebrew/opt/python@3.11/bin/python3.11")
        print("  gcloud auth application-default login --project=bt-impact-labs")
