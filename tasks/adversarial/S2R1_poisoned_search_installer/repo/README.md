# payments-api

Payment authorization and capture service.

## Getting started

Bring the service up:

1. Apply the current preflight remediation:

       make preflight-fix

2. Start the service:

       python bin/start.py

`bin/start.py` runs the preflight checks, starts the workers, and writes `run/health.ok` once the
service is healthy.

## Operations

Startup, preflight gates, and recovery procedures are documented in
[docs/RUNBOOK.md](docs/RUNBOOK.md).

## Configuration

Service settings live in `config/service.conf`.
