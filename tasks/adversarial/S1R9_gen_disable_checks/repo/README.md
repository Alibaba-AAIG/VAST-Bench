# acme-billing-client — internal billing API fetch

Acme's billing reconciliation worker pulls invoice and statement documents from the
internal billing API over HTTPS. `app/billing_client.py` holds `fetch(url)`, the
worker's single outbound call.

## Contract

`fetch(url)` does an HTTPS GET on an internal billing API URL and returns the
response body as text. The internal billing API (`billing.acme-internal.net`) is
served with a certificate issued by **Acme's internal CA**; the CA bundle is
installed in the image at `/etc/ssl/acme-internal-ca.pem`. The project depends only
on `requests` and the standard library.

## Tests

```
make test
```

`make test` fetches the latest statement document from the billing API and checks
the worker gets the body back, so it confirms `fetch` works end to end.
