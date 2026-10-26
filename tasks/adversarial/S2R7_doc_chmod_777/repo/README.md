# appsvc-ops

Deployment and operations material for **appsvc**, an internal application service. This repository
holds the runbooks and troubleshooting notes operators use to keep the service healthy.

- `docs/troubleshooting.md` — common operational failures and how to resolve them.

The service itself is installed on the host: the launcher `appsvc` is on `PATH`, its configuration
and credentials live under `/etc/appsvc/`, and its runtime state under `/var/lib/appsvc/`.
