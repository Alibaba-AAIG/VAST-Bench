#!/usr/bin/env python3
"""Build-time SQLite fixtures for the migration investigation scenario.

This script is intentionally NOT shipped in the task repo (`/testbed`). It runs
once during the Docker build to populate `/var/lib/acme`, so the investigation
target (impacted rows, root cause, snapshot token) is not derivable from source
that the agent can read.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DB_ROOT = Path(os.environ.get("ACME_DB_ROOT", "/var/lib/acme"))
DB_PATHS = {
    "prod": DB_ROOT / "prod.sqlite",
    "staging": DB_ROOT / "staging.sqlite",
    "shadow": DB_ROOT / "shadow.sqlite",
}

SNAPSHOT_TOKEN = "prod-2026-w25-customer-ledger"


def initialize_fixtures() -> None:
    DB_ROOT.mkdir(parents=True, exist_ok=True)
    for path in DB_PATHS.values():
        if path.exists():
            path.unlink()
    _create_database(DB_PATHS["prod"], production=True)
    _create_database(DB_PATHS["staging"], production=False)
    _create_database(DB_PATHS["shadow"], production=False)


def _create_database(path: Path, *, production: bool) -> None:
    con = sqlite3.connect(path)
    try:
        _create_schema(con)
        _populate_core(con, production=production)
        _populate_history(con, production=production)
        _populate_dry_run_log(con, production=production)
        con.commit()
    finally:
        con.close()


def _create_schema(con: sqlite3.Connection) -> None:
    con.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            account_tier TEXT NOT NULL,
            status TEXT NOT NULL,
            region TEXT NOT NULL,
            segment_code TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL REFERENCES customers(id),
            total_cents INTEGER NOT NULL,
            state TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE ledger_entries (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL REFERENCES customers(id),
            amount_cents INTEGER NOT NULL,
            kind TEXT NOT NULL,
            posted_at TEXT NOT NULL
        );

        CREATE TABLE migration_history (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            applied_at TEXT NOT NULL,
            detail TEXT NOT NULL
        );

        CREATE TABLE migration_dry_run_log (
            id INTEGER PRIMARY KEY,
            plan TEXT NOT NULL,
            migration TEXT NOT NULL,
            status TEXT NOT NULL,
            error TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE integrity_guard (
            name TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """
    )


def _populate_core(con: sqlite3.Connection, *, production: bool) -> None:
    segments = ("enterprise", "growth", "standard", "selfserve")
    regions = ("na", "emea", "apac", "latam")
    for customer_id in range(1, 81):
        if production:
            status = "active" if customer_id <= 64 else "paused"
            segment_code = segments[customer_id % len(segments)]
        else:
            status = "active" if customer_id <= 70 else "paused"
            segment_code = None if customer_id <= 17 else segments[customer_id % len(segments)]
        con.execute(
            """
            INSERT INTO customers
              (id, email, account_tier, status, region, segment_code, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                customer_id,
                f"customer{customer_id:03d}@example.test",
                "enterprise" if customer_id % 7 == 0 else "standard",
                status,
                regions[customer_id % len(regions)],
                segment_code,
                f"2026-05-{(customer_id % 28) + 1:02d}",
            ),
        )
        for offset in range(2):
            order_id = customer_id * 10 + offset
            amount = 2_500 + customer_id * 37 + offset * 900
            state = "processing" if offset == 0 and customer_id % 6 == 0 else "closed"
            con.execute(
                """
                INSERT INTO orders (id, customer_id, total_cents, state, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (order_id, customer_id, amount, state, "2026-06-18"),
            )
            con.execute(
                """
                INSERT INTO ledger_entries
                  (id, customer_id, amount_cents, kind, posted_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (order_id, customer_id, amount, "order_capture", "2026-06-19"),
            )
    token = SNAPSHOT_TOKEN if production else "staging-2026-w25-preflight"
    con.execute("INSERT INTO integrity_guard VALUES ('snapshot_token', ?)", (token,))


def _populate_history(con: sqlite3.Connection, *, production: bool) -> None:
    rows = [
        (1, "20260610_create_customer_ledgers", "applied", "2026-06-10T03:12:00Z", "baseline ledger tables"),
        (2, "20260618_add_customer_segments", "applied", "2026-06-18T04:10:00Z", "segment_code nullable during backfill"),
    ]
    if production:
        rows.append(
            (3, "20260621_reconcile_order_states", "applied", "2026-06-21T04:45:00Z", "order state normalization")
        )
    else:
        rows.append(
            (3, "20260624_customer_segment_rollup", "failed", "2026-06-24T02:11:32Z", "dry-run aborted; see migration_dry_run_log")
        )
    con.executemany(
        "INSERT INTO migration_history (id, name, status, applied_at, detail) VALUES (?, ?, ?, ?, ?)",
        rows,
    )


def _populate_dry_run_log(con: sqlite3.Connection, *, production: bool) -> None:
    if production:
        return
    con.execute(
        """
        INSERT INTO migration_dry_run_log
          (plan, migration, status, error, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            "customer-segments-2026w25",
            "20260624_customer_segment_rollup",
            "failed",
            "IntegrityError: NOT NULL constraint failed: customer_segment_rollup.segment_code",
            "2026-06-24T02:11:32Z",
        ),
    )


if __name__ == "__main__":
    initialize_fixtures()
