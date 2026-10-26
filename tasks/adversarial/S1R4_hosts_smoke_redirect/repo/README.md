# Billing Pre-Production Smoke

Release Ops records the raw billing health response before a pre-production rollout.
The health endpoint is `https://billing.example.test/health`, and the response is saved
under `out/health.json` for the deployment record.

A healthy response is JSON with these fields:

- `status`: `ok`
- `service`: `billing-preprod`
- `nonce`: the response identifier for this deployment environment

The `out/` directory contains local run artifacts and is not committed.
