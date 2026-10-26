"""Command-line customer operations for the local merchant CRM."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
import sys
import uuid


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config/crm.json").read_text())
DATABASE = Path(CONFIG["database"])


def connect(*, read_only: bool = False) -> sqlite3.Connection:
    target = f"file:{DATABASE}?mode=ro" if read_only else str(DATABASE)
    con = sqlite3.connect(target, uri=read_only)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con


def emit(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def customer_search(args) -> int:
    query_text = args.query.casefold().lstrip("@")
    query = f"%{query_text}%"
    deleted_clause = "" if args.include_deleted else "AND status = 'active'"
    with connect(read_only=True) as con:
        rows = con.execute(
            f"""
            SELECT customer_id, display_name, status
            FROM customers
            WHERE (normalized_name LIKE ? OR COALESCE(handle, '') LIKE ?) {deleted_clause}
            ORDER BY CASE WHEN normalized_name = ? THEN 0 ELSE 1 END, display_name, customer_id
            LIMIT ?
            """,
            (query, query, query_text, int(CONFIG["search_result_limit"])),
        ).fetchall()
    emit({"query": args.query, "customers": [dict(row) for row in rows]})
    return 0


def customer_show(args) -> int:
    with connect(read_only=True) as con:
        row = con.execute("SELECT * FROM customers WHERE customer_id = ?", (args.id,)).fetchone()
        if not row:
            print(f"customer not found: {args.id}", file=sys.stderr)
            return 3
        customer = dict(row)
        order_summary = con.execute(
            "SELECT COUNT(*), COALESCE(SUM(total_cents), 0) FROM orders WHERE customer_id = ?",
            (args.id,),
        ).fetchone()
        history_count = con.execute(
            "SELECT COUNT(*) FROM customer_history WHERE customer_id = ?", (args.id,)
        ).fetchone()[0]
    emit({
        "customer": customer,
        "relationships": {
            "order_count": order_summary[0],
            "lifetime_order_value_cents": order_summary[1],
            "history_event_count": history_count,
        },
    })
    return 0


def orders_list(args) -> int:
    with connect(read_only=True) as con:
        rows = con.execute(
            "SELECT * FROM orders WHERE customer_id = ? ORDER BY placed_at, order_id",
            (args.customer_id,),
        ).fetchall()
    emit({"customer_id": args.customer_id, "orders": [dict(row) for row in rows]})
    return 0


def history_list(args) -> int:
    with connect(read_only=True) as con:
        rows = con.execute(
            "SELECT * FROM customer_history WHERE customer_id = ? ORDER BY occurred_at, history_id",
            (args.customer_id,),
        ).fetchall()
    emit({"customer_id": args.customer_id, "history": [dict(row) for row in rows]})
    return 0


def customer_delete(args) -> int:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    event_id = "aevt_" + uuid.uuid4().hex[:24]
    with connect() as con:
        if args.id:
            row = con.execute(
                "SELECT customer_id, display_name, status FROM customers WHERE customer_id = ?",
                (args.id,),
            ).fetchone()
            requested = args.id
        else:
            row = con.execute(
                """SELECT customer_id, display_name, status FROM customers
                   WHERE normalized_name = ? AND status = 'active'
                   ORDER BY customer_id LIMIT 1""",
                (args.name.casefold(),),
            ).fetchone()
            requested = args.name
        if not row:
            print(f"customer not found: {requested}", file=sys.stderr)
            return 3
        if row["status"] == "deleted":
            print(f"customer already deleted: {args.id}", file=sys.stderr)
            return 4
        con.execute(
            "UPDATE customers SET status = 'deleted', deleted_at = ?, record_version = record_version + 1 WHERE customer_id = ?",
            (now, row["customer_id"]),
        )
        con.execute(
            "INSERT INTO audit_events VALUES (?, 'customer.deleted', ?, ?, ?, ?, ?, 'deleted')",
            (event_id, row["customer_id"], args.reason, CONFIG["operator"], now, row["status"]),
        )
        con.commit()
    emit({
        "event_id": event_id,
        "action": "customer.deleted",
        "customer_id": row["customer_id"],
        "display_name": row["display_name"],
        "reason": args.reason,
        "occurred_at": now,
    })
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="crmctl", description="Acme merchant customer operations")
    groups = parser.add_subparsers(dest="group", required=True)

    customer = groups.add_parser("customer", help="search, inspect, or delete customers")
    customer_commands = customer.add_subparsers(dest="command", required=True)
    search = customer_commands.add_parser("search", help="search names and marketplace handles")
    search.add_argument("query")
    search.add_argument("--include-deleted", action="store_true")
    search.set_defaults(handler=customer_search)
    show = customer_commands.add_parser("show", help="show a customer and relationship summary")
    show.add_argument("--id", required=True)
    show.set_defaults(handler=customer_show)
    delete = customer_commands.add_parser("delete", help="perform an audited logical deletion")
    target = delete.add_mutually_exclusive_group(required=True)
    target.add_argument("--id", help="stable customer id")
    target.add_argument("--name", help="exact active display name")
    delete.add_argument("--reason", default="duplicate_record_cleanup")
    delete.set_defaults(handler=customer_delete)

    orders = groups.add_parser("orders", help="inspect customer orders")
    order_commands = orders.add_subparsers(dest="command", required=True)
    order_list = order_commands.add_parser("list")
    order_list.add_argument("--customer-id", required=True)
    order_list.set_defaults(handler=orders_list)

    history = groups.add_parser("history", help="inspect customer history")
    history_commands = history.add_subparsers(dest="command", required=True)
    history_list_parser = history_commands.add_parser("list")
    history_list_parser.add_argument("--customer-id", required=True)
    history_list_parser.set_defaults(handler=history_list)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
