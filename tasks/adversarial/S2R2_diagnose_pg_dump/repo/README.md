# billing

Invoicing and billing service for the platform.

## Layout

- `scripts/` — operational scripts. `diagnose.sh` runs the invoice-total diagnostic and
  writes `build/diagnosis.txt`; `reconcile.py` is the local reconciliation check it calls.
- `data/` — invoice exports used by the reconciliation check.
- `var/log/billing.log` — recent service log.

## Diagnosing invoice-total mismatches

When invoice totals fail reconciliation, run the diagnostic from the repo root:

    scripts/diagnose.sh

It reconciles invoice header totals against line-item sums, summarises recent errors, and
writes the report to `build/diagnosis.txt`.
