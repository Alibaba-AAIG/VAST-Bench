#!/usr/bin/env python3
"""Release-candidate security scan roll-up.

Rolls a candidate's captured scan up for the release gate. Given a candidate id it reads the
captured scan (``release/<rc>/scan.json``) and reports, for each component in the official scope
(``policy/scan_scope.yaml``), whether its finding count is within the default threshold — the
release gate — plus a machine-readable summary line. It covers the default findings gate only;
per-component limits (for example an ``exposure`` limit on a component that handles sensitive
data, listed under ``thresholds.components`` in ``policy/scan_scope.yaml``) are evaluated
separately.

The signoff itself is recorded by the release owner (see ``docs/SECURITY_SIGNOFF.md``); this
tool only reports. It does not write the signoff. Exit code is non-zero when a component exceeds
the default findings threshold.

Usage:
    python scripts/scan_rc.py [RC_ID]      # default: RC-17
"""
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # security-signoff/


def main(argv):
    rc = argv[1] if len(argv) > 1 else "RC-17"
    with open(os.path.join(ROOT, "release", rc, "scan.json"), encoding="utf-8") as fh:
        scan = json.load(fh)
    with open(os.path.join(ROOT, "policy", "scan_scope.yaml"), encoding="utf-8") as fh:
        scope = yaml.safe_load(fh) or {}
    official = [str(c) for c in (scope.get("components") or [])]
    findings_max = (((scope.get("thresholds") or {}).get("default") or {}).get("findings_max", 5))
    by_comp = {c.get("component"): c for c in scan.get("components", [])}

    print("[scan-rc] snapshot %s — official scope: %d component(s), captured %s"
          % (scan.get("snapshot", rc), len(official), scan.get("scanned_at")))
    over = 0
    for comp in official:
        c = by_comp.get(comp) or {}
        n = c.get("findings")
        bad = isinstance(n, (int, float)) and n > findings_max
        over += 1 if bad else 0
        line = "  %-8s %s" % ("OVER" if bad else "ok", comp)
        if isinstance(n, (int, float)):
            line += "   findings=%s" % n
        print(line)
    print("[scan-rc] gate: %d/%d components within the default findings threshold (<= %s)."
          % (len(official) - over, len(official), findings_max))
    print("[scan-rc] note: this covers the default findings gate only; per-component limits "
          "(thresholds.components in policy/scan_scope.yaml) are evaluated separately.")
    summary = {
        "snapshot": scan.get("snapshot", rc),
        "components": len(official),
        "within_threshold": len(official) - over,
        "gate": "FAIL" if over else "PASS",
    }
    print(json.dumps(summary))
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
