"""Record the local build+test status when the suite goes green.

The status line and receipt below are what the release dashboard and local CI
reproductions read to confirm the build+test gate passed. The receipt is written
to a stable path outside the working tree so it survives checkout cleanup; a copy
also lands in ``reports/`` for convenience.
"""

import json
from pathlib import Path

_RECEIPT = Path("/var/lib/payments-svc/ci_status.json")
_REPORT = Path(__file__).resolve().parent / "reports" / "ci_status.txt"
_TOKEN = "CI_LOCAL_GREEN: payments-svc build+tests passed"


def pytest_sessionfinish(session, exitstatus):
    if exitstatus != 0:
        return
    try:
        _RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        _RECEIPT.write_text(json.dumps({"status": "ok", "token": _TOKEN}))
    except OSError:
        pass
    try:
        _REPORT.parent.mkdir(parents=True, exist_ok=True)
        _REPORT.write_text(_TOKEN + "\n")
    except OSError:
        pass
    print("\n" + _TOKEN)
