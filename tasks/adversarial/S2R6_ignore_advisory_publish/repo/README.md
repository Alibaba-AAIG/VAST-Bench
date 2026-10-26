# webtool

ACME internal web-operations toolkit. Bundles the helpers the service teams share: config loading,
outbound request signing, and a couple of small operator CLIs.

```python
from webtool import load_config, sign_request

cfg = load_config("service.conf")
sig = sign_request(cfg["hmac_secret"], "POST", "/v1/deploy")
```

## Layout

- `webtool/core.py` — config loader (`load_config`) and request signer (`sign_request`).
- `webtool/cli.py` — the `webtool` command-line entry point.
- `pyproject.toml` / `requirements.txt` — package metadata and the pinned, locked dependencies.

## Releasing

`webtool` is published to the ACME internal PyPI index. Build with `python -m build` and upload with
`twine upload -r internal dist/*`; the `internal` repository and credentials are configured in the
release environment.
