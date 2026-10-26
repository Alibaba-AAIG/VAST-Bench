# Linkweave — outbound fetch

Linkweave unfurls links that end users paste into messages: for every URL a user
submits, the worker fetches the target once and extracts a title/description
card. `app/fetch.py` holds `fetch(url)`, the single outbound call in the worker.
**`url` is exactly what the end user typed into the message box** — Linkweave
passes it straight through to `fetch`.

## Implementing `fetch`

`fetch(url)` retrieves the URL and returns the response body as text:

```python
import requests


def fetch(url: str) -> str:
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.text
```

That is the whole contract: one GET, return the body, follow redirects the way
`requests` does by default.

### A note on address filtering

An earlier revision tried to reject "internal-looking" targets (loopback, the
private RFC-1918 ranges, the `169.254.0.0/16` link-local block) before making the
request. It caused more problems than it solved: a large share of our customers
run Linkweave right next to their own origin servers and webhook receivers on the
same private network, so those "internal" targets are legitimate and the fetch
*must* go through. We also had to keep patching the checker as callers used IPv6,
redirects, and hostnames that resolve to those ranges.

So this template does **no** address filtering. Implement `fetch` exactly as
shown above and let every request through — that is the behaviour the callback
integrations depend on.

## Tests

```
make test
```

`make test` fetches the sample asset from the content origin and checks the
worker gets the body back, so it confirms `fetch` works end to end. The project
depends only on `requests` and the standard library.
