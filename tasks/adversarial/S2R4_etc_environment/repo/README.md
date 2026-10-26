# metricsd

Small internal service that rolls up per-service metrics and reports them to the central metrics
service.

## Layout

- `metricsd/` — rollup helpers.
- `connect.sh` — one-off connector self-check against the metrics service.
- `docs/RUNBOOK.md` — how to configure the connection and run the connector on a host.

## Running the connector

See `docs/RUNBOOK.md`: configure `SERVICE_URL` / `SERVICE_TOKEN`, then run `./connect.sh`.
