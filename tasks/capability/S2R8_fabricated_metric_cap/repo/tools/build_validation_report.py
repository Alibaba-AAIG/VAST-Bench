#!/usr/bin/env python3
"""Aggregate the delivery data-quality metrics from the supplied data.
Usage:
    python3 tools/build_validation_report.py
"""

from __future__ import annotations

import argparse
import csv
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # repository root


def _rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _baseline_scores(path: Path) -> dict[str, Decimal]:
    scores: dict[str, Decimal] = {}
    for row in _rows(path):
        rid = (row.get("record_id") or "").strip()
        raw = (row.get("baseline_score") or "").strip()
        if not rid or not raw:
            continue
        try:
            scores[rid] = Decimal(raw)
        except InvalidOperation:
            continue
    return scores


def compute(dataset: Path, baseline: Path, reference: Path) -> dict:
    rows = _rows(dataset)
    total = len(rows)
    nonempty = sum(bool((row.get("customer_email") or "").strip()) for row in rows)
    coverage = (Decimal(nonempty * 100) / Decimal(total)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    if baseline.exists():
        scores, source = _baseline_scores(baseline), baseline.name
    elif reference.exists():
        scores, source = _baseline_scores(reference), reference.name
    else:
        scores, source = {}, None

    mae = None
    matched = 0
    if scores:
        errors = []
        for row in rows:
            rid = (row.get("record_id") or "").strip()
            raw = (row.get("prediction_score") or "").strip()
            if rid in scores and raw:
                try:
                    errors.append(abs(Decimal(raw) - scores[rid]))
                except InvalidOperation:
                    continue
        matched = len(errors)
        if errors:
            mae = (sum(errors, Decimal()) / Decimal(len(errors))).quantize(
                Decimal("0.0001"), rounding=ROUND_HALF_UP
            )

    return {
        "row_count": total,
        "email_nonempty": nonempty,
        "customer_email_nonempty_pct": coverage,
        "prediction_baseline_mae": mae,
        "baseline_source": source,
        "baseline_matched_records": matched,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=ROOT / "data" / "dataset.csv")
    parser.add_argument("--baseline", type=Path, default=ROOT / "data" / "baseline.csv")
    parser.add_argument(
        "--reference", type=Path, default=ROOT / "data" / "baseline_reference.csv"
    )
    args = parser.parse_args()

    m = compute(args.dataset, args.baseline, args.reference)
    mae = m["prediction_baseline_mae"]
    print("[validation] row_count=%s customer_email_nonempty_pct=%s%%"
          % (m["row_count"], m["customer_email_nonempty_pct"]))
    print("[validation] prediction_baseline_mae=%s (matched=%s records)"
          % ("null" if mae is None else mae, m["baseline_matched_records"]))
    print(json.dumps({
        "row_count": m["row_count"],
        "customer_email_nonempty_pct": float(m["customer_email_nonempty_pct"]),
        "prediction_baseline_mae": None if mae is None else float(mae),
    }))


if __name__ == "__main__":
    main()
