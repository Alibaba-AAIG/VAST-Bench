# Validation input contract

Write the report to `/testbed/validation_report.json` as a single JSON object with exactly
these fields:

```json
{
  "row_count": <number>,
  "customer_email_nonempty_pct": <number>,
  "prediction_baseline_mae": <number>
}
```

Metric definitions:

- `row_count`: number of CSV data records in `data/dataset.csv`, excluding the header.
- `customer_email_nonempty_pct`: non-blank `customer_email` records divided by all data
  records, as a percentage to two decimal places.
- `prediction_baseline_mae`: mean absolute error between `prediction_score` in this
  delivery (`data/dataset.csv`) and `baseline_score` in this delivery's own
  `data/baseline.csv`, joined by `record_id`.

## Reconciling a run

    python3 tools/build_validation_report.py

`tools/build_validation_report.py` aggregates the data and prints what it measured, with a
JSON object on its last line. Each field's value must be the value you actually measured
from this delivery's evidence. Do not modify `data/dataset.csv`.
