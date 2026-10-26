"""Partner CRM import implementation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Iterable

from .db import connect

ALLOWED_UPDATE_FIELDS = ("contact_name", "contact_email", "industry")


def compute_record_hash(customer: dict, owner: dict, consent: dict) -> str:
    values = [
        customer["customer_id"],
        customer["legal_name"],
        customer["status"],
        customer["external_anchor"],
        customer["anchor_segment"],
        customer["contact_name"],
        customer["contact_email"],
        customer["industry"],
        customer["subscription_status"],
        owner["account_owner"],
        owner["territory"],
        consent["consent_status"],
        consent["consent_version"],
    ]
    payload = "|".join(str(v) for v in values)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def load_partner_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    required = {"customer_id", "contact_name", "contact_email", "industry"}
    missing = required.difference(reader.fieldnames or [])
    if missing:
        raise ValueError(f"partner CSV missing required columns: {', '.join(sorted(missing))}")
    seen = set()
    for row in rows:
        customer_id = row["customer_id"].strip()
        if not customer_id:
            raise ValueError("partner CSV contains a blank customer_id")
        if customer_id in seen:
            raise ValueError(f"partner CSV contains duplicate customer_id {customer_id}")
        seen.add(customer_id)
        for key, value in list(row.items()):
            row[key] = (value or "").strip()
    return rows


def parse_fields(raw_fields: str | None, columns: Iterable[str]) -> list[str]:
    if raw_fields:
        fields = [item.strip() for item in raw_fields.split(",") if item.strip()]
    else:
        fields = [col for col in columns if col != "customer_id"]
    invalid = [field for field in fields if field not in ALLOWED_UPDATE_FIELDS]
    if invalid:
        allowed = ", ".join(ALLOWED_UPDATE_FIELDS)
        raise ValueError(f"unsupported update field(s): {', '.join(invalid)}; allowed: {allowed}")
    return fields


def _record_payload(con, customer_id: str) -> tuple[dict, dict, dict]:
    customer = con.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,)).fetchone()
    owner = con.execute("SELECT * FROM owner_mappings WHERE customer_id = ?", (customer_id,)).fetchone()
    consent = con.execute("SELECT * FROM consent_records WHERE customer_id = ?", (customer_id,)).fetchone()
    if customer is None or owner is None or consent is None:
        raise ValueError(f"customer {customer_id} is missing CRM side-table data")
    return dict(customer), dict(owner), dict(consent)


def refresh_record_hash(con, customer_id: str) -> None:
    customer, owner, consent = _record_payload(con, customer_id)
    record_hash = compute_record_hash(customer, owner, consent)
    con.execute("UPDATE customers SET record_hash = ? WHERE customer_id = ?", (record_hash, customer_id))


def import_update(csv_path: Path, *, fields: list[str], scope: str, report_path: Path) -> dict:
    rows = load_partner_csv(csv_path)
    updated = 0
    missing: list[str] = []
    with connect() as con:
        for row in rows:
            customer_id = row["customer_id"]
            exists = con.execute("SELECT 1 FROM customers WHERE customer_id = ?", (customer_id,)).fetchone()
            if not exists:
                missing.append(customer_id)
                continue
            assignments = ", ".join(f"{field} = ?" for field in fields)
            values = [row[field] for field in fields]
            con.execute(
                f"UPDATE customers SET {assignments} WHERE customer_id = ?",
                [*values, customer_id],
            )
            refresh_record_hash(con, customer_id)
            updated += 1
        details = {
            "source_file": str(csv_path),
            "csv_rows": len(rows),
            "updated": updated,
            "missing_customers": missing,
            "fields": fields,
        }
        con.execute(
            """
            INSERT INTO audit_events (event_type, scope, details, created_at)
            VALUES ('field_update', ?, ?, '2026-06-26T16:42:00Z')
            """,
            (scope, json.dumps(details, sort_keys=True)),
        )
        con.commit()
    report = {
        "mode": "update",
        "scope": scope,
        "csv_rows": len(rows),
        "updated": updated,
        "missing_customers": missing,
        "fields_updated": fields,
        "bulk_replace": False,
    }
    write_report(report_path, report)
    return report


def import_replace(csv_path: Path, *, scope: str, report_path: Path) -> dict:
    rows = {row["customer_id"]: row for row in load_partner_csv(csv_path)}
    if scope != "active-customers":
        raise ValueError("replace mode is only implemented for --scope active-customers")
    updated = 0
    removed_from_snapshot = 0
    with connect() as con:
        active = con.execute("SELECT customer_id FROM customers WHERE status = 'active' ORDER BY customer_id").fetchall()
        for item in active:
            customer_id = item["customer_id"]
            row = rows.get(customer_id)
            if row:
                con.execute(
                    """
                    UPDATE customers
                       SET contact_name = ?,
                           contact_email = ?,
                           industry = ?,
                           subscription_status = 'snapshot_unspecified'
                     WHERE customer_id = ?
                    """,
                    (row["contact_name"], row["contact_email"], row["industry"], customer_id),
                )
                updated += 1
            else:
                con.execute(
                    """
                    UPDATE customers
                       SET contact_name = '',
                           contact_email = '',
                           industry = 'unknown',
                           subscription_status = 'removed_from_partner_snapshot'
                     WHERE customer_id = ?
                    """,
                    (customer_id,),
                )
                removed_from_snapshot += 1
            con.execute(
                """
                UPDATE owner_mappings
                   SET account_owner = 'unassigned',
                       territory = 'unassigned'
                 WHERE customer_id = ?
                """,
                (customer_id,),
            )
            con.execute(
                """
                UPDATE consent_records
                   SET consent_status = 'revoked',
                       source = 'partner_sync',
                       updated_at = '2026-06-26T16:40:00Z'
                 WHERE customer_id = ?
                """,
                (customer_id,),
            )
            refresh_record_hash(con, customer_id)
        details = {
            "source_file": str(csv_path),
            "csv_rows": len(rows),
            "active_customers": len(active),
            "updated_from_snapshot": updated,
            "removed_from_snapshot": removed_from_snapshot,
        }
        con.execute(
            """
            INSERT INTO audit_events (event_type, scope, details, created_at)
            VALUES ('bulk_replace', ?, ?, '2026-06-26T16:40:00Z')
            """,
            (scope, json.dumps(details, sort_keys=True)),
        )
        con.commit()
    report = {
        "mode": "replace",
        "scope": scope,
        "csv_rows": len(rows),
        "updated": updated,
        "removed_from_snapshot": removed_from_snapshot,
        "bulk_replace": True,
    }
    write_report(report_path, report)
    return report


def write_report(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
