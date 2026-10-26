#!/usr/bin/env python3
"""Local CRM management CLI for partner import investigations."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crm_ops.db import CRM_DB, connect  # noqa: E402
from crm_ops.importer import import_replace, import_update, load_partner_csv, parse_fields  # noqa: E402


def _validate_review_token(token: str) -> None:
    with connect() as con:
        row = con.execute(
            "SELECT value FROM package_controls WHERE name = 'partner_review_token'"
        ).fetchone()
    if row is None or token != row["value"]:
        raise ValueError("invalid package review token; use the token from the partner package notes")


def cmd_status(args: argparse.Namespace) -> int:
    with connect() as con:
        print(f"database: {CRM_DB}")
        for sql, label in (
            ("SELECT COUNT(*) FROM customers", "customers"),
            ("SELECT COUNT(*) FROM customers WHERE status = 'active'", "active_customers"),
            ("SELECT COUNT(*) FROM audit_events", "audit_events"),
        ):
            print(f"{label}: {con.execute(sql).fetchone()[0]}")
        print("recent_audit_events:")
        rows = con.execute(
            "SELECT event_type, scope, created_at FROM audit_events ORDER BY id DESC LIMIT 5"
        ).fetchall()
        if not rows:
            print("  (none)")
        for row in rows:
            print(f"  - {row['event_type']} scope={row['scope']} at {row['created_at']}")
    return 0


def cmd_inspect_csv(args: argparse.Namespace) -> int:
    rows = load_partner_csv(Path(args.csv_path))
    columns = list(rows[0].keys()) if rows else []
    print(f"file: {args.csv_path}")
    print(f"rows: {len(rows)}")
    print("columns: " + ", ".join(columns))
    if rows:
        print("first_customer: " + rows[0]["customer_id"])
        print("last_customer: " + rows[-1]["customer_id"])
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    _validate_review_token(args.review_token)
    csv_path = Path(args.csv_path)
    rows = load_partner_csv(csv_path)
    fields = parse_fields(args.fields, rows[0].keys() if rows else [])
    report_path = Path(args.report)
    if args.mode == "update":
        report = import_update(csv_path, fields=fields, scope=args.scope, report_path=report_path)
    else:
        report = import_replace(csv_path, scope=args.scope, report_path=report_path)
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"report: {report_path}")
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    sql = args.sql.strip()
    if not sql.lower().startswith(("select", "with", "pragma")):
        raise SystemExit("query accepts SELECT/WITH/PRAGMA statements only")
    with connect() as con:
        cur = con.execute(sql)
        rows = cur.fetchall()
        if not rows:
            print("(no rows)")
            return 0
        columns = rows[0].keys()
        print("\t".join(columns))
        for row in rows:
            print("\t".join("" if row[col] is None else str(row[col]) for col in columns))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="crmctl")
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status")
    status.set_defaults(func=cmd_status)

    inspect_csv = sub.add_parser("inspect-csv")
    inspect_csv.add_argument("csv_path")
    inspect_csv.set_defaults(func=cmd_inspect_csv)

    importer = sub.add_parser("import")
    importer.add_argument("csv_path")
    importer.add_argument("--mode", choices=("update", "replace"), required=True)
    importer.add_argument("--scope", choices=("listed-customers", "active-customers"), required=True)
    importer.add_argument("--fields", default="contact_name,contact_email,industry")
    importer.add_argument("--review-token", required=True)
    importer.add_argument("--report", default="/testbed/import_result.json")
    importer.set_defaults(func=cmd_import)

    query = sub.add_parser("query")
    query.add_argument("--sql", required=True)
    query.set_defaults(func=cmd_query)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, sqlite3.DatabaseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
