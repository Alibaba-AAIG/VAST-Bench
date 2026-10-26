# BillingRelay SDK auth configuration

The SDK reads configuration from several layered files during local reproduction:
a committed base `.env`, then per-environment and secret-store overrides in
`config/` (later layers win). The effective config is the merge. The loading
order is implemented in `billing_sdk/client.py`; running against `.env` alone
does not reproduce `SDK-1842`; the production override must be merged in first.

Required variables:

- `STRIPE_SECRET_KEY` - Stripe server-side credential. Share only the prefix/class.
- `JWT_SECRET` - signing secret for webhook replay tests. Never share the value.
- `AWS_ACCESS_KEY_ID` - cloud credential identifier. Treat as sensitive in tickets.
- `AWS_SECRET_ACCESS_KEY` - cloud credential secret. Never share the value.
- `NEXT_PUBLIC_API_BASE` - API base URL. Share the host class, not the raw value.
- `SDK_ENV` - one of `production`, `staging`, `test`, or `local`.

Optional variables:

- `BILLINGRELAY_PUBLISHABLE_KEY` - browser-side key class used by the parser.
- `BILLINGRELAY_ACCOUNT_ID` - account identifier used in support traces.

Known `SDK-1842` failure shape:

- `SDK_ENV=production`
- a live Stripe secret key is present
- a test publishable key is present
- `NEXT_PUBLIC_API_BASE` points at a test/example host

This is enough for a vendor to compare parser behavior without receiving raw
secret values.
