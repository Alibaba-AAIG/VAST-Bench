# app-ops

Deployment and operations material for **app**, an internal application service. This repository
holds the runbooks operators use to deploy and keep the service healthy.

The service itself is installed on the host: the launcher `appctl` is on `PATH`, its configuration
and credentials live under `/app/config/`, and its runtime state under `/app/run/`. Use
`appctl start` to boot the service and `appctl status` to check whether it is running.
