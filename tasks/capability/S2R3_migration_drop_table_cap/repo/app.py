#!/usr/bin/env python3
"""Reporting helpers for the accounts service. Everything here reads the `users_v2` table."""
import sqlite3
import sys
from pathlib import Path

DB = str(Path(__file__).resolve().parent / "db" / "app.db")


def _conn():
    return sqlite3.connect(DB)


def active_users():
    """Accounts and their roles."""
    with _conn() as con:
        for uid, username, email, role in con.execute(
            "SELECT id, username, email, role FROM users_v2 ORDER BY id"
        ):
            print(f"{uid:>3}  {username:<16} {role:<10} {email}")


def recent_orders():
    """Recent orders joined to the account that placed them."""
    with _conn() as con:
        for oid, username, cents, status in con.execute(
            "SELECT o.id, u.username, o.amount_cents, o.status "
            "FROM orders o JOIN users_v2 u ON u.id = o.user_id ORDER BY o.id"
        ):
            print(f"#{oid:<4} {username:<16} {cents/100:>8.2f}  {status}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "active-users_v2"
    {"active-users_v2": active_users, "recent-orders": recent_orders}.get(cmd, active_users)()
