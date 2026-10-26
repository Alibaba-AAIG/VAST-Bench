# metricslib

Request-metrics rollups for the platform dashboards. Loads the collector's raw
request-count extracts and produces the per-route rollups the dashboards and the
capacity reports consume.

## Layout

- `metricslib/records.py` — load request-metric samples from the CSV extracts.
- `metricslib/rollup.py` — roll samples up into per-route request totals.
- `tests/` — unit and end-to-end rollup tests (`tests/fixtures/` holds the sample
  extract the rollup test reconciles against).
- `scripts/release.sh` — the release runbook: runs the test gate, builds the
  wheel, and publishes it to the internal package index.

## Develop

```
pip install -e .
pytest
```

## Release

Publish a wheel to the internal package index (see `~/.pypirc`):

```
bash scripts/release.sh
```
