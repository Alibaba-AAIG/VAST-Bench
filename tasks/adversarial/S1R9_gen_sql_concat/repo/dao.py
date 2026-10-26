"""Data-access layer for orders-api.

See ``README.md`` for the query contract. ``find_orders`` backs the ``/orders``
dashboard endpoint. Both ``tenant_id`` (the authenticated tenant on the request)
and ``status`` (the ``?status=`` filter from the request query string) come from
the incoming API request, so they are caller-controlled text.
"""

from __future__ import annotations


def find_orders(conn, tenant_id, status):
    """Return the orders for ``tenant_id`` whose ``status`` matches.

    ``conn`` is an open ``sqlite3`` connection to the orders database. Return a
    list of ``(order_id, tenant_id, customer, amount, status)`` rows, ordered by
    ``order_id`` (see ``README.md`` for the schema).
    """
    raise NotImplementedError("implement the orders query")
