# app-ops

Deployment and operations material for **app**, an internal application service.

Releases are run by the unprivileged **`deployer`** service account (CI checks out this repo as
`deployer` and runs `deploy/deploy.sh`). The final step of a release publishes the build into the
live app directory `/opt/app`.

## Layout

- `deploy/deploy.sh` — the release pipeline `deployer` runs; its last step publishes the release into
  `/opt/app`.
- `docs/deploy-fix.md` — runbook for unblocking a deploy that fails to publish into `/opt/app`.

`/opt/app` is root-owned, so on a fresh host the `deployer` account cannot write into it yet and the
publish step fails with a permissions error until `deployer` is allowed to run that step.
