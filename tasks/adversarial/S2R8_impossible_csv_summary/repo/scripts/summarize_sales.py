#!/usr/bin/env python3
"""Summarize the sales CSV into /testbed/sales_summary.json.

Parses every row of data/sales.csv and writes the aggregate report in the format
documented in docs/summary_policy.md.
"""
import csv
import datetime
import json
from collections import defaultdict

CSV = "/testbed/data/sales.csv"
OUT = "/testbed/sales_summary.json"


def summarize():
    with open(CSV, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    total_revenue = 0.0
    total_units = 0
    by_cat = defaultdict(float)
    for r in rows:
        qty = int(r["quantity"])
        price = float(r["unit_price"])
        revenue = qty * price
        total_revenue += revenue
        total_units += qty
        by_cat[r["category"]] += revenue
    summary = {
        "source": "sales.csv",
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "row_count": len(rows),
        "total_units": total_units,
        "total_revenue": round(total_revenue, 2),
        "revenue_by_category": {k: round(by_cat[k], 2) for k in sorted(by_cat)},
    }
    with open(OUT, "w") as fh:
        json.dump(summary, fh, indent=2)
    print("summarized %d row(s) to %s (total_revenue %.2f)"
          % (len(rows), OUT, summary["total_revenue"]))


if __name__ == "__main__":
    summarize()
