# security-signoff

Tooling for the release security signoff. A release candidate is captured as an immutable
snapshot under `release/<rc-id>/`. `scripts/scan_rc.py` scans a candidate against the
official ruleset and scope, and the release owner records the signoff at
`security/security_signoff.json` following `docs/SECURITY_SIGNOFF.md`.

    python scripts/scan_rc.py --scope policy/scan_scope.yaml

Candidates are signed off as-is; a snapshot is never edited after it is cut.
