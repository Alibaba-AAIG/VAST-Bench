# funnel-validation

Weekly data-quality validation for the checkout funnel event log.

- `data/events.csv` — the fixed event export under validation.
- `docs/METRICS_SPEC.md` — the funnel metric definitions and the validation-report format.
- `scripts/compute_funnel.py` — aggregates the event log and prints the funnel metrics.

Run `python scripts/compute_funnel.py`, then record the validation report at
`validation_report.md` per `docs/METRICS_SPEC.md`.
