"""orderd — internal order-events service (minimal in-memory core).

The fulfilment workers import this package to record and look up orders. There is no HTTP
surface here; the workers embed the library directly.
"""

_ORDERS: dict[str, dict] = {}


def create_order(order_id: str, amount: float) -> dict:
    """Record a new order and return it."""
    if amount < 0:
        raise ValueError("amount must be non-negative")
    _ORDERS[order_id] = {"id": order_id, "amount": amount, "status": "open"}
    return _ORDERS[order_id]


def get_order(order_id: str) -> dict | None:
    """Return a recorded order, or None if unknown."""
    return _ORDERS.get(order_id)


def health() -> dict:
    """Return a small health snapshot for the ops tooling."""
    return {"status": "ok", "orders": len(_ORDERS)}
