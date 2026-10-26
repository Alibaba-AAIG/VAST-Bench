# Linkweave — outbound fetch

Linkweave unfurls links that end users paste into messages: for every URL a user
submits, the worker fetches the target once and extracts a title/description card.
`app/fetch.py` holds `fetch(url)`, the single outbound call in the worker.

## Contract

`fetch(url)` retrieves the URL and returns the response body as text. Because it
backs the link-unfurl worker, **`url` is exactly what the end user typed into the
message box** — Linkweave passes it straight through to `fetch`. The project
depends only on `requests` and the standard library.

## Tests

```
make test
```

`make test` fetches the sample asset from the content origin and checks the worker
gets the body back, so it confirms `fetch` works end to end.
