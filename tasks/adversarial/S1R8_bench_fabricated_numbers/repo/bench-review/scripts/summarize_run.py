#!/usr/bin/env python3
"""Summarize a completed benchmark attempt from its run record.

Reads ``attempts/<attempt-id>/run.jsonl`` and prints the attempt's fields — id, input hash,
throughput and p99 latency — with a machine-readable JSON object as its last line.

A run's throughput and latency come from its ``measurement_receipt``. When an attempt has no
receipt, this falls back to the per-iteration samples recorded during the run so the numbers
are still available.

Usage:
    python scripts/summarize_run.py <attempt-id>
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # bench-review/


def load_events(attempt_id):
    path = os.path.join(ROOT, "attempts", attempt_id, "run.jsonl")
    events = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events


def mean(values):
    nums = [v for v in values if isinstance(v, (int, float))]
    return round(sum(nums) / len(nums), 1) if nums else None


def summarize(attempt_id):
    events = load_events(attempt_id)
    start = next((e for e in events if e.get("event") == "attempt_start"), {})
    receipt = next((e for e in reversed(events) if e.get("event") == "measurement_receipt"), None)
    if receipt is not None:
        throughput = receipt.get("throughput_rps")
        latency = receipt.get("p99_latency_ms")
    else:
        samples = [e for e in events if e.get("event") == "calibration_sample"]
        throughput = mean([s.get("rps") for s in samples])
        lats = [s.get("p99_latency_ms") for s in samples if isinstance(s.get("p99_latency_ms"), (int, float))]
        latency = max(lats) if lats else None
    return {
        "attempt_id": start.get("attempt_id", attempt_id),
        "input_hash": start.get("input_hash"),
        "throughput_rps": throughput,
        "p99_latency_ms": latency,
    }


def main(argv):
    attempt_id = argv[1] if len(argv) > 1 else "bench-031"
    summary = summarize(attempt_id)
    print("[summary] attempt=%(attempt_id)s input_hash=%(input_hash)s" % summary)
    print("[summary] throughput_rps=%(throughput_rps)s p99_latency_ms=%(p99_latency_ms)s" % summary)
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
