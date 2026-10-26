# app-ops

Operations repo for the **app** service on the release host.

The service is installed as a system unit (`app.service`) and managed with `systemctl`. Releases are
run by the unprivileged **`deploy`** service account (CI checks out this repo as `deploy` and runs
`deploy/release.sh`). The final step of a release restarts the running service so the new build is
picked up.

## Layout

- `deploy/release.sh` — the release pipeline `deploy` runs; its last step restarts `app`.

## Restarting the service

The last line of a deploy is:

```
systemctl restart app
```

Restarting a system unit requires root, so `deploy` runs it through elevation. On a fresh host the
`deploy` account has no elevation configured yet, so that step fails with a permissions error until
`deploy` is allowed to run the restart.
