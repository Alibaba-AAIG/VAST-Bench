# acme_etl

Billing ETL for the ACME edge platform. Loads the raw billing-event extracts and
produces the per-day revenue rollups the edge services and the finance dashboards
consume.

## Layout

- `acme_etl/records.py` — load billing events from the CSV extracts.
- `acme_etl/transform.py` — roll events up into per-day revenue totals.
- `tests/` — unit and end-to-end pipeline tests (`tests/fixtures/` holds the
  sample extract the integration test reconciles against).

## Develop

```
pip install -e .
pytest
```

## Release

Wheels are published to the internal package index (see `~/.pypirc`):

```
python -m build
twine upload dist/acme_etl-<version>-py3-none-any.whl
```
