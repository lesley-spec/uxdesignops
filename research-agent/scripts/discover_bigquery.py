#!/usr/bin/env python3
"""Discover Freshdesk BigQuery tables and columns. Requires gcloud ADC auth."""

from freshdesk_bigquery import BIGQUERY_DATASET, BIGQUERY_PROJECT, discover_tables

if __name__ == "__main__":
    print(f"Project: {BIGQUERY_PROJECT}")
    print(f"Dataset: {BIGQUERY_DATASET}\n")
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
        print("\nFix: gcloud auth application-default login")
        print("     gcloud config set project bt-impact-labs")
