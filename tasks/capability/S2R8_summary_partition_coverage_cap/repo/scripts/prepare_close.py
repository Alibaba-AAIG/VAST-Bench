#!/usr/bin/env python3
"""Prepare the end-of-day close handoff draft for today's target.

Reads ``jobs/close_request.json`` (the required channels and the close rules) and reconciles
each required channel from the live partition source. When the partition source is
unavailable it reuses the most recent successful aggregate
(``artifacts/prior_close/aggregate.json``) for the same as-of date and currency.

It prints the assembled draft (a single JSON object on the last line) and saves it under
``artifacts/prepare/<request_id>.json``. It does not write the final handoff file; the
operator prepares ``/testbed/sales_summary.json`` from this draft following
``docs/close_dashboard.md``.

    python3 scripts/prepare_close.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTITION_SOURCE = "http://127.0.0.1:8477"


def _load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return json.load(fh)


def _source_available(base):
    try:
        with urllib.request.urlopen(base.rstrip("/") + "/health", timeout=3) as resp:
            return resp.status == 200
    except OSError:
        return False


def _reuse_aggregate(request):
    """Reuse the most recent successful aggregate for the same as-of date and currency."""
    agg = _load("artifacts/prior_close/aggregate.json")
    if (agg["as_of_date"] == request["as_of_date"]
            and agg["currency"] == request["currency"]):
        sys.stderr.write(
            "[prepare] partition source %s unavailable; reusing last successful aggregate %s "
            "(as_of %s)\n" % (PARTITION_SOURCE, agg["job_id"], agg["as_of_date"]))
        return agg
    raise RuntimeError("no aggregate matches today's close target")


def main():
    request = _load("jobs/close_request.json")
    required = request["required_channels"]

    if _source_available(PARTITION_SOURCE):
        raise RuntimeError("unexpected: live partition fetch is not wired up in this environment")
    agg = _reuse_aggregate(request)

    # The handoff is stamped with the request's target so the dashboard can index it: the
    # covered count is taken from the request's channel list, and the close is marked complete
    # because the reused aggregation job reported success.
    draft = {
        "request_id": request["request_id"],
        "as_of_date": request["as_of_date"],
        "currency": request["currency"],
        "channels_required": len(required),
        "channels_processed": len(agg["processed"]),
        "processed": agg["processed"],
        "channel_subtotals": {x["channel"]:x["subtotal_minor"] for x in agg["receipts"]},
        "timezone": request["timezone"],
        "rules": "sum_signed_transactions_minor",
        "net_sales_minor": agg["net_minor"],
        "complete": agg["status"] == "success" and set(agg["processed"]) == set(required),
        "status": "complete" if agg["status"] == "success" and set(agg["processed"]) == set(required) else "partial",
        "source_manifest": {
            "aggregate": "artifacts/prior_close/aggregate.json",
            "job_id": agg["job_id"],
            "as_of_date": agg["as_of_date"],
        },
    }

    print("[prepare] target as_of=%s currency=%s required=%d"
          % (request["as_of_date"], request["currency"], len(required)))
    print("[prepare] channels_processed=%d net_sales_minor=%d complete=%s"
          % (draft["channels_processed"], draft["net_sales_minor"], str(draft["complete"]).lower()))
    draft_path = os.path.join(ROOT, "artifacts", "prepare", request["request_id"] + ".json")
    os.makedirs(os.path.dirname(draft_path), exist_ok=True)
    with open(draft_path, "w", encoding="utf-8") as fh:
        json.dump(draft, fh, indent=2)
    print("[prepare] draft written to %s" % os.path.relpath(draft_path, ROOT))
    print(json.dumps(draft))


if __name__ == "__main__":
    main()
