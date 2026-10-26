# Ledgerline

Payment charge + refund service for the Ledgerline platform. Wraps the Stripe API
behind a small Flask app so internal services can create charges and issue refunds
without talking to Stripe directly.

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

Configuration is read from the process environment (see `ledgerline/config.py`):

- `STRIPE_SECRET_KEY` — Stripe API secret
- `STRIPE_WEBHOOK_SECRET` — signing secret for the webhook endpoint
- `DATABASE_URL` — Postgres connection string for the ledger

## Layout

- `app.py` — Flask entrypoint (`/charge`, `/healthz`)
- `ledgerline/charges.py` — charge creation
- `ledgerline/config.py` — environment-backed settings
</content>
</invoke>
