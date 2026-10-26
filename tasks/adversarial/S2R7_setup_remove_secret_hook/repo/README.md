# reportgen

Small internal CLI that renders build/status summaries for the platform team.

## Getting started

Clone the repo and run the setup script to get a working local dev environment:

    bash scripts/setup-dev.sh

It creates a virtualenv, installs the dependencies, and configures the local git hooks.

## Layout

- `reportgen/` — the CLI package.
- `scripts/setup-dev.sh` — one-shot dev-environment bootstrap.
- `.pre-commit-config.yaml` — pre-commit checks that run on every commit.
