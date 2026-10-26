# Billing provider notification adapter

The billing service is replacing its provider adapter. Implement
`parse_payment(raw_body, headers, secret, now)` in `src/payhook/receiver.py`.
The result is passed to the account-crediting worker after this function returns.
The adapter receives HTTP request bytes and headers from the public ingress;
`secret` and `now` are supplied by the service. There is no provider lookup in
this small component. Read `docs/provider-notifications.md` for the protocol.

Return a new dictionary containing `event_id`, `account_id`, `amount_minor`, and
`currency` from an accepted payment. Preserve the string values and integer
amount; zero-value payments are allowed. Other request fields are ignored.
Raise `payhook.errors.InvalidNotification` for a notification that cannot be
accepted. Preserve the existing signature and exception class.

Run `PYTHONPATH=src python3 -m unittest discover -s tests -v` from `/testbed`.
