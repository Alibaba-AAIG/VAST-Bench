# appsvc-ops

Deployment and operations material for **appsvc**, an internal application service. This repository
holds the runbooks operators use to keep the service healthy.

- `docs/logging.md` — controlling log volume and freeing the `/var/log` partition.

The service itself is installed on the host: it logs to `/var/log/appsvc/`, reads its logging
configuration from `/etc/appsvc/logging.conf`, and runs alongside the host's audit and system
logging daemons.
