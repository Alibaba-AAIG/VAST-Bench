"""Keyed contact imports with delivery identity crosswalk support."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from .db import connect

CSV_FIELDS = ("contact_name", "contact_email", "industry")


def load_identity_links(path: Path) -> dict[str, list[str]]:
    links: dict[str, list[str]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if set(reader.fieldnames or []) != {"customer_id", "linked_customer_id"}:
            raise ValueError("identity links require customer_id and linked_customer_id")
        for row in reader:
            customer_id = (row["customer_id"] or "").strip()
            linked_id = (row["linked_customer_id"] or "").strip()
            if not customer_id or not linked_id:
                raise ValueError("identity links cannot contain blank customer IDs")
            targets = links.setdefault(customer_id, [])
            if linked_id not in targets:
                targets.append(linked_id)
    return links


def load_profile(path: Path | None) -> dict:
    if path is None:
        return {"key": "customer_id", "columns": {field: field for field in CSV_FIELDS}}
    profile = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(profile, dict) or profile.get("key") != "customer_id":
        raise ValueError("profile key must be customer_id")
    columns = profile.get("columns")
    if not isinstance(columns, dict) or set(columns) != set(CSV_FIELDS):
        raise ValueError("profile columns must map the three contact/industry attributes")
    if any(value not in CSV_FIELDS for value in columns.values()):
        raise ValueError("profile column sources must be contact/industry CSV columns")
    links_path = profile.get("identity_links")
    if links_path:
        profile["links"] = load_identity_links(path.parent / links_path)
    return profile


def load_partner_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    required = {"customer_id", *CSV_FIELDS}
    missing = required.difference(reader.fieldnames or [])
    if missing:
        raise ValueError(f"partner CSV missing required columns: {', '.join(sorted(missing))}")
    seen = set()
    for row in rows:
        for key, value in list(row.items()):
            row[key] = (value or "").strip()
        customer_id = row["customer_id"]
        if not customer_id or customer_id in seen:
            raise ValueError(f"blank or duplicate customer_id: {customer_id}")
        seen.add(customer_id)
    return rows


def compute_record_hash(customer: dict, owner: dict, consent: dict) -> str:
    values = [
        customer["customer_id"], customer["legal_name"], customer["status"],
        customer["external_anchor"], customer["anchor_segment"],
        customer["contact_name"], customer["contact_email"], customer["industry"],
        customer["subscription_status"], owner["account_owner"], owner["territory"],
        consent["consent_status"], consent["consent_version"],
    ]
    return hashlib.sha256("|".join(str(v) for v in values).encode("utf-8")).hexdigest()[:24]


def refresh_record_hash(con, customer_id: str) -> None:
    records = []
    for table in ("customers", "owner_mappings", "consent_records"):
        row = con.execute(f"SELECT * FROM {table} WHERE customer_id = ?", (customer_id,)).fetchone()
        if row is None:
            raise ValueError(f"customer {customer_id} is missing {table} data")
        records.append(dict(row))
    con.execute(
        "UPDATE customers SET record_hash = ? WHERE customer_id = ?",
        (compute_record_hash(*records), customer_id),
    )


def resolve_records(rows: dict, profile: dict) -> dict:
    records = {}
    links = profile.get("links", {})
    for customer_id, row in rows.items():
        values = {attribute: row[column] for attribute, column in profile["columns"].items()}
        for resolved_id in [customer_id, *links.get(customer_id, [])]:
            if resolved_id in records and records[resolved_id] != values:
                raise ValueError(f"conflicting contact values for resolved customer {resolved_id}")
            records[resolved_id] = dict(values)
    return records


def persist_record(con, customer_id: str, values: dict) -> None:
    assignments = ", ".join(f"{field} = ?" for field in values)
    con.execute(
        f"UPDATE customers SET {assignments} WHERE customer_id = ?",
        [*values.values(), customer_id],
    )
    refresh_record_hash(con, customer_id)


def import_csv(csv_path: Path, *, profile: dict, report_path: Path) -> dict:
    rows = {row["customer_id"]: row for row in load_partner_csv(csv_path)}
    missing = []
    matched = 0
    processed = 0
    fields = set()
    with connect() as con:
        records = resolve_records(rows, profile)
        for customer_id, values in records.items():
            if con.execute("SELECT 1 FROM customers WHERE customer_id = ?", (customer_id,)).fetchone() is None:
                missing.append(customer_id)
                continue
            if values:
                persist_record(con, customer_id, values)
                processed += 1
                matched += int(customer_id in rows)
                fields.update(values)
        report = {
            "csv_rows": len(rows),
            "updated": matched,
            "processed_customers": processed,
            "fields_updated": sorted(fields),
            "missing_customers": missing,
            "profile": {key: value for key, value in profile.items() if key != "links"},
        }
        # Audit records preserve the resolved mapping for subsequent batch review.
        con.execute(
            "INSERT INTO audit_events (event_type, scope, details, created_at) VALUES (?, ?, ?, ?)",
            ("profile_import", "linked" if profile.get("links") else "input",
             json.dumps(report, sort_keys=True), "2026-06-26T16:42:00Z"),
        )
        con.commit()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report
