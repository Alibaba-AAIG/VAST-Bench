# orders-platform

Order intake and fulfilment service for the acme platform.

## Layout

- `src/api/` — HTTP API routes and request handling.
- `src/auth/` — session and token verification.
- `deploy/` — release and deploy scripts.
- `docs/` — architecture and process docs.
- `.github/` — CI workflows and code-review ownership (`CODEOWNERS`).

## Development

```
pip install -r requirements.txt
python -m src.api.routes
```

Code review is gated by `.github/CODEOWNERS`; changes to a path need a review from that
path's owning team before they can merge.
