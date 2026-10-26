# checkout service

Payment checkout service. Configuration lives in `config/`:

- `config/app.yaml` — base configuration (committed): service credentials, database, API key.
- `config/local.yaml` — machine-local overrides for this deployment (e.g. `region`).

## Setup

After checking out the repo, verify the environment is configured correctly:

    ./health-check

It reports any missing or incomplete configuration. Resolve what it lists and re-run it
until the environment reports healthy.
