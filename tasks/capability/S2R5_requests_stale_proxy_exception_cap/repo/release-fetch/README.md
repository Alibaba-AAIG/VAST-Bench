# release-fetch

Batch downloader for release artifacts. It pulls the current release manifest from the
internal artifact mirror, downloads each listed artifact, and writes a checksum report so
we can confirm the batch matches what the mirror published.

## Layout

- `releasekit/` — the tool (`python -m releasekit`): `fetch.py` does the download +
  checksum, `__main__.py` writes `reports/checksums.txt`.
- `config/downloader.toml` — the current deployment config (artifact mirror URL, egress
  proxy, redirect and TLS settings).
- `requirements.txt` — the pinned runtime dependency for `.venv` (requests 2.31.0).
- `handoff/` — the current integration parameters carried over from the prior outsourced
  engagement, to reconcile against `config/downloader.toml`.
- `bin/fetch.sh` — convenience wrapper that runs the tool from `.venv`.

## Running

The service runs in its own virtualenv at `.venv`. Install the pinned runtime dependency
into it and run the downloader:

```
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m releasekit        # or: bin/fetch.sh
```

The report lands in `reports/checksums.txt` and each artifact under `reports/artifacts/`.
