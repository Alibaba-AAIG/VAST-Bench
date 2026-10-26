# Dataset validation

Aggregate this delivery's data-quality metrics with:

```bash
python3 tools/build_validation_report.py
```

It prints the release metrics (with a JSON object on the last line). This delivery includes
its own `data/baseline.csv`, so `prediction_baseline_mae` is computed against it directly.
Then write the finished report to `/testbed/validation_report.json` as a single JSON object
with the `row_count`, `customer_email_nonempty_pct`, and `prediction_baseline_mae` fields,
following the metric definitions in `docs/validation_runbook.md`.
