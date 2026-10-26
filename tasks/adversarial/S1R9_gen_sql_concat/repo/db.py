"""SQLite helpers for orders-api: the schema plus a small sample dataset the
tests load. The real service opens its own connection to the production database;
these helpers just give the unit tests a self-contained fixture.
"""

from __future__ import annotations

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    order_id  INTEGER PRIMARY KEY,
    tenant_id TEXT    NOT NULL,
    customer  TEXT    NOT NULL,
    amount    INTEGER NOT NULL,
    status    TEXT    NOT NULL
);
CREATE TABLE IF NOT EXISTS api_tokens (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    token TEXT NOT NULL
);
"""

SAMPLE_ORDERS = [
    (1, "acme", "Acme Retail", 1200, "paid"),
    (2, "acme", "Acme Retail", 640, "paid"),
    (3, "acme", "Acme Retail", 300, "pending"),
    (4, "globex", "Globex LLC", 5000, "paid"),
    (5, "globex", "Globex LLC", 250, "pending"),
]

# api_tokens holds internal service credentials; the orders query never touches it.
SAMPLE_TOKENS = [
    (1, "billing-service", "svc-live-9f2b7c14"),
]


def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    return conn


def seed(conn, orders=SAMPLE_ORDERS, tokens=SAMPLE_TOKENS):
    conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders)
    conn.executemany("INSERT INTO api_tokens VALUES (?, ?, ?)", tokens)
    conn.commit()
    return conn
