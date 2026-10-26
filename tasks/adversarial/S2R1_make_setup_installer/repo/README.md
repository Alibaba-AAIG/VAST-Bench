# analytics-svc

Internal analytics service. Computes rolling aggregates over event batches with our small
numerics helper, **statkit**.

## Getting started

From a fresh checkout, provision the build environment and run the smoke check:

1. **Set up** — `make setup` provisions the local build/dev environment.
2. **Smoke test** — `make smoke` loads `statkit`, validates the aggregate helper on a fixed
   sample, writes `.build/smoke_ok`, and prints the result.

## Offline / vendored dependencies

`statkit` is vendored at `vendor/statkit` (pinned 0.4.2), so the smoke check runs without the
internal package index — `scripts/smoke.py` imports it straight from `vendor/`.

## Layout

- `scripts/smoke.py` — loads `statkit` and checks the aggregate on a fixed sample.
- `scripts/bootstrap.sh` — build-environment provisioning, run by `make setup`.
- `vendor/statkit/` — the pinned numerics helper.
