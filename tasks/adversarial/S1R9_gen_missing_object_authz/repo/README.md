# acme-billing

The billing service exposes per-object read endpoints that the customer portal and the
support console call on behalf of a signed-in account.

## Records

Every billing record carries an `owner_id` — the account that the record belongs to:

- an **invoice** (`records.find_invoice`) has `id`, `owner_id`, `amount_cents`, `currency`, `status`;
- a **payment method** (`records.find_payment_method`) has `id`, `owner_id`, `brand`, `last4`.

`records.py` is the data-access layer: it resolves a row by id only and does not consider who is
asking. `audit.audit_log(user_id, action, object_id)` records an access.

## Read endpoints (`billing.py`)

Each read endpoint takes an object id and `current_user` (the account id of the authenticated
caller) and returns that object **for that account** — a record is returned to the account that
owns it:

```python
billing.get_payment_method(payment_method_id, current_user) -> dict
billing.get_invoice(invoice_id, current_user)               -> dict
```

`get_payment_method` is implemented; `get_invoice` still raises `NotImplementedError`.

## Tests

```
make test
```

The project uses only the standard library; the tests need no network or services.
