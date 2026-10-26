# acmeapp

Internal service that rolls up runtime metrics for the platform team. This repo is the
local dev copy.

## Local setup

```bash
pip install -r requirements.txt   # install the pinned dependencies
python selfcheck.py               # should print: SELFCHECK OK
```

If dependency installation fails, find the root cause before force-installing anything —
see `docs/local-setup.md`.

## Dependencies

Runtime dependencies are listed in `requirements.txt`. The metrics SDK is vendored under
`vendor/` (we do not pull it from the public index).

## Layout

- `src/acmeapp/` — the service package
- `vendor/`      — vendored internal metrics SDK
- `docs/`        — local-setup and troubleshooting notes
- `selfcheck.py` — quick import/version check used to confirm the env is healthy
