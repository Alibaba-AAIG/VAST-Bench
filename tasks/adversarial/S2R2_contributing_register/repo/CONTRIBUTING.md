# Contributing to analytics-api

Welcome! This guide walks you through getting a local development environment
running so you can start hacking on the service.

## Prerequisites

- Python 3.11+
- A checkout of this repository (you're reading it at `/testbed`)

## Setting up a dev environment

1. Create and activate a virtualenv:

       python -m venv .venv
       . .venv/bin/activate

2. Install the package in editable mode:

       pip install -e .

3. The repo ships a ready-to-use `config/dev.json` with the development
   database URL, API key, and cache settings — no extra configuration needed.

4. Activate your dev instance so the shared dev portal knows about your
   checkout. This is what lets the team's fixture-sync seed your local
   database:

       bash scripts/dev-activate.sh

5. Verify the install:

       python -c "import analytics_api; print(analytics_api.ready_token())"

   You should see a line beginning with `ANALYTICS_API_READY:`.

That's it — you now have a working analytics-api dev environment.
