#!/usr/bin/env python3
"""Official suite client (invoked by run_all.sh).

Drives the local integration daemon over every case in tests/cases.json, in
order, then writes the report JSON atomically once the full run completes.
"""

import json
import os
import sys
import time
import urllib.request

CONFIG_PATH = "/testbed/tests/testsvc_config.json"
CASES_PATH = "/testbed/tests/cases.json"


def _post(base, path, token, obj):
    data = json.dumps(obj).encode("utf-8")
    request = urllib.request.Request(
        base + path,
        data=data,
        headers={"Content-Type": "application/json", "X-Test-Token": token},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "/testbed/test_report.json"
    with open(CONFIG_PATH, encoding="utf-8") as fh:
        cfg = json.load(fh)
    with open(CASES_PATH, encoding="utf-8") as fh:
        cases = json.load(fh)

    base = f"http://{cfg['host']}:{cfg['port']}"
    token = cfg["token"]
    run_id = os.environ.get("RUN_ID") or f"run-{int(time.time())}"

    results = []
    for case in cases:
        res = _post(base, "/run", token, {"run": run_id, "case": case})
        results.append({"id": res["id"], "status": res["status"]})
    _post(base, "/complete", token, {"run": run_id, "count": len(results)})

    passed = sum(1 for r in results if r["status"] == "pass")
    failed = len(results) - passed
    report = {
        "suite": "orders-integration",
        "runner": "tests/run_all.sh",
        "generated_by": "official-pipeline",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "run_id": run_id,
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "status": "all_passed" if failed == 0 else "failed",
        "cases": results,
    }
    tmp = out_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    os.replace(tmp, out_path)
    print(f"wrote {out_path}: {passed} passed, {failed} failed of {len(results)}")


if __name__ == "__main__":
    main()
