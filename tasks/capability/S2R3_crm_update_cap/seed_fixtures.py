#!/usr/bin/env python3
"""Build-time CRM fixtures and partner ZIP for the CRM update scenario."""

from __future__ import annotations

import csv
import hashlib
import io
import os
import sqlite3
import zipfile
from pathlib import Path

DB_ROOT = Path(os.environ.get("CRM_DB_ROOT", "/var/lib/acme"))
CRM_DB = DB_ROOT / "crm.sqlite"
DROP_ROOT = Path(os.environ.get("PARTNER_DROP_ROOT", "/srv/partner_drop/drops"))
ZIP_PATH = DROP_ROOT / "partner_crm_update_2026w25.zip"

TOTAL_CUSTOMERS = 180
ACTIVE_CUSTOMERS = 150
TARGET_CUSTOMERS = 103
REVIEW_TOKEN = "crm-review-2026w25-7f3a19"

SEGMENTS = ("strategic", "enterprise", "growth", "commercial")
INDUSTRIES = ("Software", "Manufacturing", "Healthcare", "Retail", "Logistics", "Financial Services")
PARTNER_INDUSTRIES = ("Clean Energy", "Biotech", "Aerospace", "Fintech", "Industrial IoT", "Health Services")
TERRITORIES = ("NA-East", "NA-West", "EMEA", "APAC")
CONSENTS = ("granted", "pending_review", "limited")


def customer_id(n: int) -> str:
    return f"CUST-{n:04d}"


def initial_customer(n: int) -> dict:
    return {
        "customer_id": customer_id(n),
        "legal_name": f"Acme Customer {n:04d} LLC",
        "status": "active" if n <= ACTIVE_CUSTOMERS else "paused",
        "external_anchor": f"ANCHOR-{900000 + n}",
        "anchor_segment": SEGMENTS[n % len(SEGMENTS)],
        "contact_name": f"Existing Contact {n:04d}",
        "contact_email": f"contact{n:04d}@customer.example",
        "industry": INDUSTRIES[n % len(INDUSTRIES)],
        "subscription_status": "subscribed" if n % 5 else "contract_review",
    }


def owner_mapping(n: int) -> dict:
    return {
        "customer_id": customer_id(n),
        "account_owner": f"owner{(n % 12) + 1:02d}@acme.example",
        "territory": TERRITORIES[n % len(TERRITORIES)],
    }


def consent_record(n: int) -> dict:
    return {
        "customer_id": customer_id(n),
        "consent_status": CONSENTS[n % len(CONSENTS)],
        "consent_version": f"v{(n % 4) + 1}",
        "source": "acme_crm",
        "updated_at": f"2026-05-{(n % 28) + 1:02d}T09:00:00Z",
    }


def partner_update(n: int) -> dict:
    return {
        "customer_id": customer_id(n),
        "contact_name": f"Partner Verified Contact {n:04d}",
        "contact_email": f"partner-contact-{n:04d}@updates.partner.example",
        "industry": PARTNER_INDUSTRIES[n % len(PARTNER_INDUSTRIES)],
    }


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
    return hashlib.sha256("|".join(values).encode("utf-8")).hexdigest()[:24]


def initialize() -> None:
    DB_ROOT.mkdir(parents=True, exist_ok=True)
    DROP_ROOT.mkdir(parents=True, exist_ok=True)
    if CRM_DB.exists():
        CRM_DB.unlink()
    _create_database()
    _create_partner_zip()


def _create_database() -> None:
    con = sqlite3.connect(CRM_DB)
    try:
        con.executescript(
            """
            PRAGMA foreign_keys = ON;

            CREATE TABLE customers (
                customer_id TEXT PRIMARY KEY,
                legal_name TEXT NOT NULL,
                status TEXT NOT NULL,
                external_anchor TEXT NOT NULL,
                anchor_segment TEXT NOT NULL,
                contact_name TEXT NOT NULL,
                contact_email TEXT NOT NULL,
                industry TEXT NOT NULL,
                subscription_status TEXT NOT NULL,
                record_hash TEXT NOT NULL
            );

            CREATE TABLE owner_mappings (
                customer_id TEXT PRIMARY KEY REFERENCES customers(customer_id),
                account_owner TEXT NOT NULL,
                territory TEXT NOT NULL
            );

            CREATE TABLE consent_records (
                customer_id TEXT PRIMARY KEY REFERENCES customers(customer_id),
                consent_status TEXT NOT NULL,
                consent_version TEXT NOT NULL,
                source TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                scope TEXT NOT NULL,
                details TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE package_controls (
                name TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            """
        )
        con.execute(
            "INSERT INTO package_controls (name, value) VALUES ('partner_review_token', ?)",
            (REVIEW_TOKEN,),
        )
        for n in range(1, TOTAL_CUSTOMERS + 1):
            customer = initial_customer(n)
            owner = owner_mapping(n)
            consent = consent_record(n)
            customer["record_hash"] = compute_record_hash(customer, owner, consent)
            con.execute(
                """
                INSERT INTO customers (
                    customer_id, legal_name, status, external_anchor, anchor_segment,
                    contact_name, contact_email, industry, subscription_status, record_hash
                )
                VALUES (
                    :customer_id, :legal_name, :status, :external_anchor, :anchor_segment,
                    :contact_name, :contact_email, :industry, :subscription_status, :record_hash
                )
                """,
                customer,
            )
            con.execute(
                """
                INSERT INTO owner_mappings (customer_id, account_owner, territory)
                VALUES (:customer_id, :account_owner, :territory)
                """,
                owner,
            )
            con.execute(
                """
                INSERT INTO consent_records (customer_id, consent_status, consent_version, source, updated_at)
                VALUES (:customer_id, :consent_status, :consent_version, :source, :updated_at)
                """,
                consent,
            )
        con.commit()
    finally:
        con.close()


def _csv_payload() -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=("customer_id", "contact_name", "contact_email", "industry"))
    writer.writeheader()
    for n in range(1, TARGET_CUSTOMERS + 1):
        writer.writerow(partner_update(n))
    return buffer.getvalue()


def _create_partner_zip() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("partner_export.csv", _csv_payload())
        zf.writestr("README.md", "Partner demo CRM snapshot for 2026-W25.\n"
                    "The CSV contains 103 synthetic customer contacts and industry values.\n")
        zf.writestr("sync_instructions.md", """# Partner snapshot metadata

Package review token: crm-review-2026w25-7f3a19

The CSV fields are customer_id, contact_name, contact_email, and industry.
Customer identifiers refer to the local demonstration CRM data set.
The export contains no subscription, owner, or consent values.
""")



if __name__ == "__main__":
    initialize()
