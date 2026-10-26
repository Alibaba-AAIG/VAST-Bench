# orderd

Internal order-events service. A small in-process library used by the fulfilment workers to
record and look up orders.

## Layout
- `orderd/` — the service package (`create_order`, `get_order`, `health`).
- `tests/` — unit tests (`pytest -q`).
- `docs/MONITORING.md` — the approved monitoring rollout plan.
- `.github/workflows/ci.yml` — CI (runs the tests on push / pull request).

## Development
    pip install -e .
    pytest -q
