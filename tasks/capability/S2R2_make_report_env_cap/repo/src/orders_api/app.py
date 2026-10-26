"""Minimal request router for the Orders service."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Order:
    id: int
    sku: str
    qty: int


class OrderStore:
    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}
        self._next = 1

    def create(self, sku: str, qty: int) -> Order:
        order = Order(id=self._next, sku=sku, qty=qty)
        self._orders[order.id] = order
        self._next += 1
        return order

    def get(self, order_id: int) -> Order | None:
        return self._orders.get(order_id)

    def list(self) -> list[Order]:
        return list(self._orders.values())


def database_url() -> str:
    return os.environ.get("DATABASE_URL", "postgresql://localhost/orders")


def health() -> dict[str, str]:
    return {"status": "ok", "service": "orders-api"}
