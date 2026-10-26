# flowgate

A small reverse-proxy / API gateway that fronts our internal services: connection
pooling, upstream TLS, and a drain path for graceful shutdown.

## Layout

- `gateway.py` — request routing and the upstream connection pool.
- `pool.conf` / `tls.conf` — runtime tuning for the pool and upstream TLS.
- `RELEASES.md` — release / branch tracking.

## Development

```
pip install -r requirements.txt
python gateway.py
```

Cut a `release/*` branch per shipped version; hotfixes go on `hotfix/*` and are merged
back into `main` once verified.
