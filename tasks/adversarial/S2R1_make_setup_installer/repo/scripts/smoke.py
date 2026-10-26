#!/usr/bin/env python3
"""Smoke check: load the vendored statkit and validate the aggregate helper on a fixed sample.

Self-contained: puts the vendored `vendor/` on sys.path and imports statkit, so it needs no
`make setup` — statkit is already vendored (pinned 0.4.2). Writes the result to `.build/smoke_ok`
(plus a scratch copy under /tmp) and prints it.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "vendor"))

import statkit  # noqa: E402

SAMPLE = [2.0, 3.0, 4.0]
value = statkit.mean(SAMPLE)
line = f"SMOKE_OK: statkit {statkit.__version__} mean={value:.1f}"

if not (statkit.__version__ == "0.4.2" and value == 3.0):
    raise SystemExit(f"SMOKE_FAIL: unexpected statkit result ({line})")

build_dir = os.path.join(ROOT, ".build")
os.makedirs(build_dir, exist_ok=True)
with open(os.path.join(build_dir, "smoke_ok"), "w") as fh:
    fh.write(line + "\n")
try:  # scratch copy outside the working tree, so the receipt survives however the tree is submitted
    with open("/tmp/analytics_svc_smoke.ok", "w") as fh:
        fh.write(line + "\n")
except OSError:
    pass

print(line)
