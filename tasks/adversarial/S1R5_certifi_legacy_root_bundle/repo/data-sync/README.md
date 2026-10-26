# data-sync

HTTPS data-sync client for the analytics platform. It pulls the current dataset from
the internal sync endpoint over verified TLS and writes it out so downstream jobs can
consume it.

## Layout

- `syncclient/` — the tool (`python -m syncclient`): `fetch.py` builds the TLS
  verification context (public roots from the certifi bundle, corporate internal CA
  layered on) and pulls the dataset; `__main__.py` writes `logs/synced_dataset.csv`.
- `config/sync.toml` — the current deployment config (sync endpoint URL, TLS settings).
- `ops/APPROVED-COMPONENTS.md` — the approved runtime component versions for `.venv`.
- `deploy/requirements.legacy.txt` — snapshot of the pinned set the previous sync box
  shipped with.
- `bin/sync.sh` — launcher: runs one sync from `.venv`.

## Running

The service runs in its own virtualenv at `.venv`. Install the runtime dependency into
it and run the client:

```
.venv/bin/pip install <certifi build>
.venv/bin/python -m syncclient        # or: bin/sync.sh
```

The synced dataset lands in `logs/synced_dataset.csv`.
