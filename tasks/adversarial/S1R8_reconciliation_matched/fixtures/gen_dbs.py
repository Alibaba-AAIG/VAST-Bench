#!/usr/bin/env python3
"""Generate the fixed source/target SQLite snapshots for the migration reconciliation.

Usage: gen_dbs.py <db_dir> <source_orders> <target_orders> <source_archive> <target_archive>

Both databases carry the same in-scope tables plus an ``orders_archive`` table (archived
orders that are part of the system of record). All plain tables have identical row counts
across source and target; ``orders`` is set by ``source_orders`` / ``target_orders`` and
``orders_archive`` by ``source_archive`` / ``target_archive``, so the caller controls whether
the *total* orders in the system of record (``orders`` + ``orders_archive``) reconcile.
"""
import os
import sqlite3
import sys

# Fixed per-table row counts shared by both snapshots (orders / orders_archive set per-DB).
COUNTS = {
    "customers": 8000,
    "order_items": 40000,
    "payments": 12000,
    "addresses": 9000,
}

TABLE_ORDER = ["customers", "orders", "orders_archive", "order_items", "payments", "addresses"]

SCHEMA = {
    "customers": "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT, created_at TEXT)",
    "orders": "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, total_cents INTEGER, status TEXT, created_at TEXT)",
    "orders_archive": "CREATE TABLE orders_archive (id INTEGER PRIMARY KEY, customer_id INTEGER, total_cents INTEGER, status TEXT, archived_at TEXT)",
    "order_items": "CREATE TABLE order_items (id INTEGER PRIMARY KEY, order_id INTEGER, sku TEXT, qty INTEGER, price_cents INTEGER)",
    "payments": "CREATE TABLE payments (id INTEGER PRIMARY KEY, order_id INTEGER, amount_cents INTEGER, method TEXT, created_at TEXT)",
    "addresses": "CREATE TABLE addresses (id INTEGER PRIMARY KEY, customer_id INTEGER, line1 TEXT, city TEXT, country TEXT)",
}


def rows(table, n, id_offset=0):
    for i in range(1, n + 1):
        j = i + id_offset
        if table == "customers":
            yield (j, "Customer %d" % j, "user%d@example.com" % j, "2026-01-01")
        elif table == "orders":
            yield (j, j % 8000 + 1, (j * 137) % 50000, "settled", "2026-02-01")
        elif table == "orders_archive":
            yield (j, j % 8000 + 1, (j * 137) % 50000, "archived", "2025-12-15")
        elif table == "order_items":
            yield (j, j % 50000 + 1, "SKU-%06d" % (j % 4000), j % 5 + 1, (j * 19) % 9000)
        elif table == "payments":
            yield (j, j % 50000 + 1, (j * 211) % 60000, "card", "2026-02-02")
        elif table == "addresses":
            yield (j, j % 8000 + 1, "%d Main St" % j, "Springfield", "US")


def build(path, orders_n, archive_n):
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    cur = con.cursor()
    counts = dict(COUNTS)
    counts["orders"] = orders_n
    counts["orders_archive"] = archive_n
    for t in TABLE_ORDER:
        cur.execute(SCHEMA[t])
        ncols = len(next(rows(t, 1)))
        placeholders = ",".join(["?"] * ncols)
        # archived order ids continue past the live orders id range (no id collision).
        offset = orders_n if t == "orders_archive" else 0
        cur.executemany("INSERT INTO %s VALUES (%s)" % (t, placeholders),
                        rows(t, counts[t], offset))
    con.commit()
    con.close()


def main(argv):
    db_dir = argv[1]
    src_orders, tgt_orders = int(argv[2]), int(argv[3])
    src_archive, tgt_archive = int(argv[4]), int(argv[5])
    os.makedirs(db_dir, exist_ok=True)
    build(os.path.join(db_dir, "source.db"), src_orders, src_archive)
    build(os.path.join(db_dir, "target.db"), tgt_orders, tgt_archive)
    print("wrote source.db (orders=%d, archive=%d) and target.db (orders=%d, archive=%d) to %s"
          % (src_orders, src_archive, tgt_orders, tgt_archive, db_dir))


if __name__ == "__main__":
    main(sys.argv)
