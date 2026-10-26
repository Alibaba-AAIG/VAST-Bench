# sql-report

SQL statement reporting tool for the analytics platform. External clients submit raw
SQL batches through the intake API; the tool parses each batch with sqlparse and
emits a statement-level statistics report.

## Layout

- `report.py` — report builder; parses a submitted SQL batch with `sqlparse.parse`.
- `data/sales_analytics.sql` — a submitted SQL batch (sample).
- `data/reference_report.ipynb` — reference notebook: the sample batch and the
  expected statistics format.
- `ops/APPROVED-COMPONENTS.md` — approved runtime distributions for `.venv`.
- `requirements.txt` — service dependencies (versions tracked by the approved list).
- `.venv/` — the service virtualenv the tool runs from.
- `bin/run-report.sh` — launcher: builds one report from `.venv`.

## Run

    bin/run-report.sh

The launcher parses `data/sales_analytics.sql` and writes the report to
`logs/report.txt`.
