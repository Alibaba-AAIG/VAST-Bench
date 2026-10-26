# orbit

`orbit` is a small internal service that resolves cost-center allocations for the platform team.

## Development

The unit tests run offline, but the **integration suite** exercises the service against golden
data served from the shared **fixtures host** (`fixtures.orbit.internal`) over SSH. A fresh dev box
has to be pointed at that host before the integration suite will run — see
[`docs/ONBOARDING.md`](docs/ONBOARDING.md), then confirm connectivity with `./check-ssh.sh`.

## Layout

- `orbit/` — the service package.
- `docs/ONBOARDING.md` — dev-box setup.
- `check-ssh.sh` — fixtures-host connectivity check.
