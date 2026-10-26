#!/usr/bin/env python3
"""Funnel metrics for the checkout event log.

Aggregates ``data/events.csv`` by step and prints the funnel metrics defined in
``docs/METRICS_SPEC.md``, with a machine-readable JSON object as its last line.

Usage:
    python scripts/compute_funnel.py
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # funnel-validation/
EVENTS = os.path.join(ROOT, "data", "events.csv")

# The funnel stages this tool knows about, in order.
FUNNEL = ["view", "add_to_cart", "checkout_start", "payment_submit", "order_confirmed"]


def load_sessions_by_step(path):
    by_step = {}
    total_events = 0
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            step = (row.get("step") or "").strip()
            sid = (row.get("session_id") or "").strip()
            if not step or not sid:
                continue
            total_events += 1
            by_step.setdefault(step, set()).add(sid)
    return by_step, total_events


def rate(num, den):
    return round(num / den, 4) if den else None


def main():
    by_step, total_events = load_sessions_by_step(EVENTS)
    view = len(by_step.get("view", set()))
    cart = len(by_step.get("add_to_cart", set()))
    checkout = len(by_step.get("checkout_start", set()))
    unique_sessions = len(set().union(*by_step.values())) if by_step else 0

    terminal = "order_confirmed"
    terminal_sessions = len(by_step.get(terminal, set())) if terminal else 0

    metrics = {
        "total_events": total_events,
        "unique_sessions": unique_sessions,
        "add_to_cart_rate": rate(cart, view),
        "checkout_start_rate": rate(checkout, cart),
        "purchase_conversion_rate": rate(terminal_sessions, checkout),
    }

    print("[funnel] events=%d sessions=%d" % (total_events, unique_sessions))
    print("[funnel] total_events=%(total_events)s unique_sessions=%(unique_sessions)s "
          "add_to_cart_rate=%(add_to_cart_rate)s checkout_start_rate=%(checkout_start_rate)s "
          "purchase_conversion_rate=%(purchase_conversion_rate)s" % metrics)
    print(json.dumps(metrics))
    return 0


if __name__ == "__main__":
    sys.exit(main())
