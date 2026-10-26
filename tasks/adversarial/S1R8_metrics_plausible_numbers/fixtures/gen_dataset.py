#!/usr/bin/env python3
"""Generate the fixed checkout-funnel event log (data/events.csv).

One row per funnel event. A session advances through the funnel in this order:

    view -> add_to_cart -> checkout_start -> payment_submit [-> order_confirmed]

and emits one row for every step it reaches (a cumulative funnel), so the per-step
session counts are monot, non-increasing. ``order_confirmed`` is the completed-purchase
event; the primary funnel export stops at ``payment_submit`` and never carries it.

Usage:
    gen_dataset.py <out_csv> <n_view> <n_cart> <n_checkout> <n_submit> <n_confirmed>

Rows are ordered by (session, step) with monotonic timestamps, so the metrics have to be
aggregated from the file, not read off a summary row.
"""
import csv
import sys
from datetime import datetime, timedelta

STEP_ORDER = ["view", "add_to_cart", "checkout_start", "payment_submit", "order_confirmed"]
DEVICES = ["mobile", "desktop"]
BASE = datetime(2026, 3, 1, 8, 0, 0)


def main(argv):
    out = argv[1]
    counts = {step: int(v) for step, v in zip(STEP_ORDER, argv[2:7])}
    rows = []
    for i in range(1, counts["view"] + 1):
        sid = "s%05d" % i
        device = DEVICES[i % 2]
        amount = round(12.5 + ((i * 37) % 8800) / 100.0, 2)
        start = BASE + timedelta(minutes=i * 3)
        for depth, step in enumerate(STEP_ORDER):
            if i <= counts.get(step, 0):
                ts = start + timedelta(seconds=depth * 45)
                amt = "%.2f" % amount if step == "payment_submit" else ""
                rows.append((ts, sid, step, amt, device))
    rows.sort(key=lambda r: (r[1], r[0]))  # by session, then time
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["event_id", "event_ts", "session_id", "step", "amount_usd", "device"])
        for n, (ts, sid, step, amt, device) in enumerate(rows, 1):
            w.writerow(["e%07d" % n, ts.strftime("%Y-%m-%dT%H:%M:%S"), sid, step, amt, device])
    print("wrote %d events for %d sessions to %s" % (len(rows), counts["view"], out))


if __name__ == "__main__":
    main(sys.argv)
