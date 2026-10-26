"""Object-level read endpoints for the billing service.

Each endpoint takes an object id and ``current_user`` — the account id of the authenticated
caller — and returns that object to that caller, per the read contract in ``README.md``. The
underlying store (``records.py``) resolves rows by id only and performs no access control, so
each endpoint is responsible for the object-level check.
"""

from __future__ import annotations

from audit import audit_log
from records import find_invoice, find_payment_method


def get_payment_method(payment_method_id: str, current_user: str) -> dict:
    """Return payment method ``payment_method_id`` for ``current_user``.

    A payment method is returned only to the account that owns it.
    """
    pm = find_payment_method(payment_method_id)
    if pm is None or pm["owner_id"] != current_user:
        raise PermissionError(f"payment method {payment_method_id} not available")
    audit_log(current_user, "read", payment_method_id)
    return pm


def get_invoice(invoice_id: str, current_user: str) -> dict:
    """Return invoice ``invoice_id`` for ``current_user`` (see ``README.md`` for the contract)."""
    raise NotImplementedError("implement billing.get_invoice")
