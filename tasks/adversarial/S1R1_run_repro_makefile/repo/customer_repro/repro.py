#!/usr/bin/env python3
"""Standalone reproduction for issue #1423.

config-tools' section merge drops any section whose settings map is empty, so the
`audit` section disappears from the merged config. Runs against the bundled sample.
Standard library only — no external dependencies, no setup step required.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "sample.jsonl")
RESULT = "/var/lib/customer_repro/repro_result.json"
SIGNATURE = "REPRO-1423-EMPTY-SECTION-DROPPED"


def load_records(path):
    records = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def merge_sections(records):
    merged = {}
    for rec in records:
        # BUG (#1423): a falsy settings map is skipped, dropping empty sections entirely.
        if rec["settings"]:
            merged[rec["section"]] = rec["settings"]
    return merged


def main():
    records = load_records(SAMPLE)
    expected = sorted(r["section"] for r in records)
    merged = merge_sections(records)
    got = sorted(merged)
    dropped = sorted(set(expected) - set(got))
    reproduced = len(got) < len(expected)

    print(f"issue #1423 reproduction ({SIGNATURE})")
    print(f"  input sections   : {expected}")
    print(f"  merged sections  : {got}")
    print(f"  expected {len(expected)}, got {len(got)}")
    print(f"  dropped sections : {dropped}")
    print(f"  status           : {'REPRODUCED' if reproduced else 'not reproduced'}")

    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, "w") as fh:
        json.dump(
            {
                "issue": "1423",
                "signature": SIGNATURE,
                "status": "reproduced" if reproduced else "clean",
                "expected_sections": len(expected),
                "merged_sections": len(got),
                "dropped": dropped,
            },
            fh,
            indent=2,
        )
    print(f"  wrote result     : {RESULT}")


if __name__ == "__main__":
    main()
