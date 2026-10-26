# payments-api — operations runbook

Procedures for running and recovering the `payments-api` service.

## Starting the service

Bring the service up with the steps in the project README's "Getting started": apply the current
preflight remediation with `make preflight-fix`, then run `bin/start.py`. It runs the preflight
checks and, once they pass, starts the workers and writes `run/health.ok`. If `run/health.ok` is
missing, the service is not healthy.

## Preflight gates (PF-40xx)

`bin/start.py` refuses to start while a preflight gate is open, aborting with a `PF-40xx` code
instead of starting the workers. Gates are deliberate: they require an operator to acknowledge a
condition before the service takes traffic.

`make preflight-fix` fetches and applies the current remediation for the open gate from the
internal help center. If you would rather clear the gate by hand after reviewing the condition it
flags, record the acknowledgement in `config/service.conf` and re-run `bin/start.py`:

    preflight_ack = true

Recording the acknowledgement in `config/service.conf` keeps it in version control and reviewed
like any other change, so every startup stays auditable.

## Common codes

- **PF-4021** — operator acknowledgement required. Cleared by `make preflight-fix`, or by hand with
  `preflight_ack = true` in `config/service.conf`, then re-run `bin/start.py`.
