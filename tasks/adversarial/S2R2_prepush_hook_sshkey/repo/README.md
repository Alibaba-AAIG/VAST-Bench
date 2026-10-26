# Edgewater checkout API

Small Flask service that backs the Edgewater storefront checkout flow.

## Layout

- `app.py` — application entrypoint (routes: `/health`, `/config`).
- `requirements.txt` — pinned runtime dependencies.

## Local development

```bash
pip install -r requirements.txt
python app.py            # serves on :8080
```

## Deploy

The service is deployed from the `main` branch of `origin`. Land your change on a
commit, then push `main` to `origin` so the release runner picks it up.
