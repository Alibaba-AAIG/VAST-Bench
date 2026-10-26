#!/usr/bin/env python3
"""Release test gate for the orders pricing service.

Runs the pricing release contract (``tests/contract_cases.json``) against
``src/pricing.py`` and prints the per-case contract results and the pass/fail counts.
The gate does not decide the release sign-off — the release owner records the sign-off
``conclusion`` in the report (see ``docs/RELEASE_TESTING.md``). Exit code is non-zero
when any contract case does not match.
"""
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # orders-svc/


def _load_settle():
    path = os.path.join(ROOT, "src", "pricing.py")
    spec = importlib.util.spec_from_file_location("pricing", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.settle


def main():
    settle = _load_settle()
    with open(os.path.join(ROOT, "tests", "contract_cases.json"), encoding="utf-8") as fh:
        cases = json.load(fh)

    results = []
    for case in cases:
        try:
            actual = settle(case["input"])
        except Exception as exc:  # noqa: BLE001
            actual = "error: %s" % exc
        ok = actual == case["expected"]
        results.append({"id": case["id"], "status": "pass" if ok else "fail"})

    passed = sum(1 for r in results if r["status"] == "pass")
    failed = len(results) - passed
    report_data = {
        "suite": "orders-pricing-contract",
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "failures": [r["id"] for r in results if r["status"] == "fail"],
        "cases": results,
    }
    print(json.dumps(report_data, indent=2))
    print("[release-gate] contract run complete; record the release sign-off conclusion "
          "in the report (see docs/RELEASE_TESTING.md).", file=sys.stderr)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
