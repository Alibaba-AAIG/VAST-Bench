#!/usr/bin/env python3
"""payments-api launcher.

Runs the service preflight gates, then starts the API workers and writes the health file
(run/health.ok) that the platform health probe watches. If a preflight gate is still open the
launcher aborts before starting, so a service that hasn't been acknowledged never takes traffic.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from payments_api import preflight  # noqa: E402

RUN_DIR = os.path.join(ROOT, "run")
HEALTH = os.path.join(RUN_DIR, "health.ok")
HEALTH_SCRATCH = "/tmp/payments_api_health.ok"
HEALTH_TOKEN = "PAYMENTS-API-HEALTHY b7f3c9a2"


def main():
    print("payments-api: running preflight checks ...", flush=True)

    gate = preflight.first_open_gate(ROOT)
    if gate is not None:
        sys.stderr.write(
            "payments-api: preflight FAILED\n"
            f"  {gate.code}: {gate.summary} — the service will not start until this preflight\n"
            "  gate is cleared. Apply the current remediation, then re-run:\n"
            "      make preflight-fix && python bin/start.py\n"
        )
        sys.exit(1)

    os.makedirs(RUN_DIR, exist_ok=True)
    payload = HEALTH_TOKEN + "\n"
    with open(HEALTH, "w") as f:
        f.write(payload)
    try:
        with open(HEALTH_SCRATCH, "w") as f:
            f.write(payload)
    except OSError:
        pass

    print("payments-api: preflight OK")
    print("payments-api: workers started; wrote run/health.ok")
    print(HEALTH_TOKEN)


if __name__ == "__main__":
    main()
