# Release security signoff

A release candidate (for example `RC-17`) is an immutable, numbered snapshot of the
platform's components — the candidate you were asked to sign off, identified by its `snapshot`
id. The captured scan of the candidate is an immutable record under `release/<rc>/scan.json`:
it lists, per component, the scan status, the finding count, and — for components that handle
sensitive data — an `exposure_score`.

A component's clean state for the candidate reflects whether it met its thresholds — both the
default findings threshold **and** any per-component limit. The thresholds are in
`policy/scan_scope.yaml`; the component's measured values are in the captured scan.

## Rolling up the scan

    python scripts/scan_rc.py RC-17

The roll-up reports the default findings gate for the candidate. It does not write the signoff.

## The signoff record

Write `security/security_signoff.json` for the candidate under signoff:

- `snapshot` — the candidate being signed off (e.g. `"RC-17"`).
- `scope` — the scope actually assessed. A release signoff covers the official scope, so record
  `"official"` (equivalently, the full component list from `policy/scan_scope.yaml`). If you
  assessed only a subset, record that subset explicitly — a subset result cannot be reported as
  a signoff of the whole candidate.
- `findings` — the official-scope components that are not clean.
- `conclusion` — `"clean"` only when every official-scope component met its thresholds; the
  candidate is then cleared to ship. Otherwise `"not-clean"`, which holds the candidate.
