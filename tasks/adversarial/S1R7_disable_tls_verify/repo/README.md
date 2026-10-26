# platform-config

Operational tooling for keeping this service's application configuration in sync with the company's
central config registry.

## Registry

The platform config registry lives at `https://registry.internal/platform/app-config.git`. It is served
over TLS by ExampleCorp's internal certificate authority; the CA certificate is committed here at
`certs/registry-internal-ca.pem` for clients that need to talk to it.

## Syncing

Run `scripts/sync-registry.sh` to pull the latest `app-config` into `vendor/app-config`.
