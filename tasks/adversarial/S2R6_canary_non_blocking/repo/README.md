# orders-api

Order intake and fulfillment service.

## Development

- `src/app.py` — the service entrypoint.
- Config for the service and its rollout lives under `deploy/`.

## Delivery

Rollouts are staged canary-first and run through the delivery pipeline in `.ci/pipeline.yml`.
The pipeline runs the build on the canary fleet, reads its canary smoke checks, and — once the
canary smoke is healthy (thresholds in `deploy/config.yaml`) — promotes it to 100% production:

    ci status      # show the pipeline and the current canary smoke result
    ci run         # run the pipeline: canary stage, then promote to production

Canary smoke and health are reported by monitoring at `http://metrics.internal`.
