# orders-api

Order intake and fulfillment service.

## Development

- `src/app.py` — the service entrypoint.
- Config for the service and its rollout lives under `deploy/`.

## Deployment

Rollouts are staged canary-first. The CI pipeline ships each build to the canary fleet; once the
canary smoke checks are confirmed healthy (thresholds in `deploy/config.yaml`), the build is promoted
to production:

    ./deploy.sh status      # current rollout state + canary smoke summary
    ./deploy.sh smoke       # full canary smoke checks for the current build
    ./deploy.sh prod        # promote the current canary build to 100% production
    ./deploy.sh rollback    # roll the canary build back

Canary smoke and health are reported by monitoring at `http://metrics.internal`.
