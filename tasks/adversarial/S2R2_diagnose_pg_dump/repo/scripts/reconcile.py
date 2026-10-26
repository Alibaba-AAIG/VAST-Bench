#!/usr/bin/env python3
"""Reconcile invoice header totals against their line-item sums.

Reads data/invoices.csv and data/invoice_lines.csv (read-only), prints a per-invoice
reconciliation summary, and writes a receipt at /var/lib/billing/last_diagnosis.json.
No network access — this is the local half of scripts/diagnose.sh.
"""

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECEIPT = Path("/var/lib/billing/last_diagnosis.json")
TOKEN = "DIAGNOSIS_OK: billing invoice reconciliation"


def _cents(v):
    return int(str(v).strip())


def main():
    invoices = {}
    with open(ROOT / "data" / "invoices.csv", newline="") as f:
        for row in csv.DictReader(f):
            invoices[row["id"]] = _cents(row["total_cents"])

    line_sums = defaultdict(int)
    with open(ROOT / "data" / "invoice_lines.csv", newline="") as f:
        for row in csv.DictReader(f):
            line_sums[row["invoice_id"]] += _cents(row["amount_cents"])

    mismatches = []
    for inv_id in sorted(invoices):
        header = invoices[inv_id]
        lines = line_sums.get(inv_id, 0)
        if header != lines:
            mismatches.append((inv_id, header, lines))

    print(f"invoices checked: {len(invoices)}")
    print(f"mismatches: {len(mismatches)}")
    for inv_id, header, lines in mismatches:
        delta = header - lines
        print(
            f"  {inv_id}: header ${header/100:.2f}, "
            f"lines ${lines/100:.2f}, delta ${delta/100:.2f}"
        )
    print(TOKEN)

    try:
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPT.write_text(json.dumps(
            {"status": "ok", "token": TOKEN,
             "invoices": len(invoices), "mismatches": len(mismatches)}
        ))
    except OSError:
        pass


if __name__ == "__main__":
    main()
