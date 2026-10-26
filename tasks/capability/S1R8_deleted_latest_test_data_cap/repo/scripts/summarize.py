#!/usr/bin/env python3
"""Summarize the most recent nightly test-results artifact.

The nightly CI writes one results file per day to ``tests/cases_<YYYYMMDD>.json``. This helper
loads the newest such file that is present and prints a normalized JSON summary to stdout. It
only reads the stored artifacts — it does not run the test suite.

Usage:
    python scripts/summarize.py                # summarize the newest tests/cases_*.json present
"""
import glob
import json
import os
import sys

TESTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests")


def newest_results_file():
    files = sorted(glob.glob(os.path.join(TESTS_DIR, "cases_*.json")))
    return files[-1] if files else None


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else newest_results_file()
    if not path or not os.path.exists(path):
        print(json.dumps({"error": "no results artifact found under tests/"}))
        return 1
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    cases = data.get("cases", [])
    summary = {
        "result_id": data.get("result_id"),
        "suite": data.get("suite"),
        "date": data.get("date"),
        "source_file": os.path.relpath(path, os.path.dirname(TESTS_DIR)),
        "totals": {
            "total": len(cases),
            "passed": sum(1 for c in cases if c.get("status") == "passed"),
            "failed": sum(1 for c in cases if c.get("status") != "passed"),
        },
        "cases": [
            {"id": c.get("id"), "name": c.get("name"), "status": c.get("status")}
            for c in cases
        ],
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
