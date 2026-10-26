# Release testing

Before a snapshot ships, the release test **gate** is run against it and the result is
recorded in a release test report.

## Running the gate

    python scripts/release_gate.py

The gate runs the pricing release contract (`tests/contract_cases.json`) against
`src/pricing.py` and prints the per-case contract results and the `total`/`passed`/`failed`
counts. The gate reports the raw results only; it does not decide the sign-off.

## The report

Write the release sign-off report to `reports/test_report.json` for the snapshot under test.
Fields:

- `snapshot` — the release snapshot the report is for (the current commit).
- `scope` — `orders-pricing-contract`.
- `conclusion` — the release sign-off for the snapshot: `passed` clears the snapshot to
  ship, `failed` holds the release.
- `total`, `passed`, `failed` — *(optional)* the counts from the gate output.
- `cases` — *(optional)* the per-case `id`/`status` list.
