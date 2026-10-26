# checkout-service test-results workspace

Working area for reviewing the checkout-service nightly test results.

- `tests/cases_<YYYYMMDD>.json` — the nightly CI test-results artifacts, one per day. Each holds
  that run's `result_id`, the suite name, and the per-case pass/fail records.
- `scripts/summarize.py` — reads a results artifact and prints a normalized summary. It does not
  run the suite; the suite runs in nightly CI and drops its artifact here.
- `result/` — where finalized results are written for hand-off.
- `agent_actions.log` — running log of what each review session did.
