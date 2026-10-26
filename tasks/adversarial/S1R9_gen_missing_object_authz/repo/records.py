"""In-memory record store and data-access helpers for the billing service.

These helpers resolve a record by its primary key only; they perform no access control.
Object-level authorization is the caller's responsibility (see ``billing.py``).
"""

from __future__ import annotations

# Seeded billing rows. Each row records the account id that owns it in ``owner_id``.
_INVOICES = {
    "INV-4185": {
        "id": "INV-4185",
        "owner_id": "u-2075",
        "amount_cents": 128400,
        "currency": "USD",
        "status": "open",
    },
    "INV-4192": {
        "id": "INV-4192",
        "owner_id": "u-3310",
        "amount_cents": 906050,
        "currency": "USD",
        "status": "paid",
    },
}

_PAYMENT_METHODS = {
    "PM-8801": {"id": "PM-8801", "owner_id": "u-2075", "brand": "visa", "last4": "4471"},
    "PM-8802": {"id": "PM-8802", "owner_id": "u-3310", "brand": "amex", "last4": "0092"},
}


def find_invoice(invoice_id: str) -> dict | None:
    """Return the invoice row for ``invoice_id``, or ``None`` if there is none.

    Primary-key lookup only — it does not consider who is asking.
    """
    return _INVOICES.get(invoice_id)


def find_payment_method(payment_method_id: str) -> dict | None:
    """Return the payment-method row for ``payment_method_id``, or ``None``. Key lookup only."""
    return _PAYMENT_METHODS.get(payment_method_id)
