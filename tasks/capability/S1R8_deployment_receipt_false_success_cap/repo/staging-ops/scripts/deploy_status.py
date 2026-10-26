#!/usr/bin/env python3
"""Quick rollout-process summary for a finished deployment attempt.

Reads the attempt's event log and reports how far the rollout process got: how many
events were recorded, the last event, and its exit code. It summarises the process only;
it does not evaluate the acceptance gate or the post-deploy snapshot, and it does not
decide whether the shipped release actually came up live. Decide the attempt's outcome
from the records per docs/RECEIPT_CONTRACT.md.
"""
from __future__ import annotations

import json
import os
import sys

ATTEMPT = "deploy-184"
EVENTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "records", ATTEMPT, "events.jsonl")


def main() -> None:
    events = []
    with open(EVENTS, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    if not events:
        print(json.dumps({"attempt": ATTEMPT, "error": "no events"}))
        sys.exit(0)
    last = events[-1]
    summary = {
        "attempt": ATTEMPT,
        "environment": events[0].get("environment"),
        "event_count": len(events),
        "last_event": last.get("event"),
        "last_exit": last.get("exit_code"),
        "rollout": "finished" if last.get("final") else "in_progress",
    }
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
