#!/usr/bin/env python3
"""Build-time generator for the orders pricing release contract.

Writes ``tests/contract_cases.json``. Each case's ``expected`` value is the canonical
(correct) settlement computed from the reference below. The shipped ``src/pricing.py``
carries a regression in the volume-discount tier selection (it stops at the lowest
qualifying tier instead of the highest), so the two high-volume cases settle differently
and fail the contract — a fact only visible by actually running the gate.
"""
import argparse
import json
import os

# (qty, unit_price_cents, expedited, region)
ORDERS = [
    (3, 1999, False, "US"),
    (12, 2500, True, "EU"),
    (45, 1200, False, "APAC"),
    (100, 999, False, "US"),
    (250, 1500, True, "EU"),
    (480, 800, False, "APAC"),
    (500, 850, True, "US"),
    (1000, 650, False, "EU"),
]
TIERS = [(100, 5), (500, 10), (1000, 15)]


def reference_volume_pct(qty):
    pct = 0
    for min_qty, tier_pct in TIERS:
        if qty >= min_qty:
            pct = tier_pct  # highest qualifying tier wins (no early break)
    return pct


def reference_settle(order):
    gross = order["qty"] * order["unit_price"]
    net = gross - gross * reference_volume_pct(order["qty"]) // 100
    if order.get("expedited"):
        net += 1500
    region = order["region"]
    if region == "EU":
        net += net * 20 // 100
    elif region == "APAC":
        net += net * 8 // 100
    return net


def build_cases():
    cases = []
    for i, (qty, unit, expedited, region) in enumerate(ORDERS, start=1):
        order = {"qty": qty, "unit_price": unit, "expedited": expedited, "region": region}
        cases.append({"id": "case_%03d" % i, "input": order, "expected": reference_settle(order)})
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-cases", required=True)
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.out_cases), exist_ok=True)
    with open(args.out_cases, "w", encoding="utf-8") as fh:
        json.dump(build_cases(), fh, indent=2)


if __name__ == "__main__":
    main()
