# Meridian Artifact Fetcher

Meridian Artifact Fetcher prepares release bundles for downstream deployment
workers. It reads a small source catalog, fetches each bundle into a staging
directory, and emits a manifest summary that release automation can archive.

## Readiness Check

The refreshed worker image starts with an empty Go module cache. After repairing
module state, run the readiness check from the repository root:

```bash
./scripts/check_fetcher.sh
```

The check validates the dependency safety floor recorded in source, builds the
commands, fetches the configured bundle, and verifies the resulting manifest.
