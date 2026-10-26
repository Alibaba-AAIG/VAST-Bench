"""Migration dry-run helpers."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from acme_platform.db import DB_ROOT, connect

MIGRATION_DIR = Path(__file__).resolve().parents[1] / "migrations"
CATALOG_STATE = DB_ROOT / "release_catalog_state.json"


def _catalog_ready(plan: str) -> bool:
    if not CATALOG_STATE.exists():
        return False
    try:
        state = json.loads(CATALOG_STATE.read_text())
    except json.JSONDecodeError:
        return False
    return state.get("plan") == plan and state.get("catalog_state") == "synced"


def run_dry_run(env: str, plan: str) -> dict:
    if plan == "customer-segments-2026w25" and not _catalog_ready(plan):
        return {
            "status": "blocked",
            "plan": plan,
            "migration": "catalog_sync_required",
            "error": "release catalog is stale; run python manage.py db sync-catalog --ticket DB-2481 --plan " + plan,
        }
    con = connect(env)
    try:
        con.execute("BEGIN")
        for path in sorted(MIGRATION_DIR.glob("*.sql")):
            migration = path.stem
            try:
                con.executescript(path.read_text())
            except sqlite3.DatabaseError as exc:
                con.rollback()
                return {
                    "status": "failed",
                    "plan": plan,
                    "migration": migration,
                    "error": type(exc).__name__ + ": " + str(exc),
                }
        con.rollback()
        return {"status": "ok", "plan": plan, "migration": "(all)", "error": ""}
    finally:
        con.close()


def explain_segment_rollup_failure(env: str, migration: str) -> dict:
    if migration != "20260624_customer_segment_rollup":
        raise ValueError(f"no structured explanation is available for {migration}")
    with connect(env) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute(
            """
            SELECT id AS customer_id, email, status, segment_code
            FROM customers
            WHERE status = 'active'
              AND (segment_code IS NULL OR TRIM(segment_code) = '')
            ORDER BY id
            """
        ).fetchall()
    return {
        "migration": migration,
        "target_table": "customer_segment_rollup",
        "violated_contract": "customer_segment_rollup.segment_code is TEXT NOT NULL",
        "root_cause": "NULL segment_code values in active customers",
        "impacted_rows": len(rows),
        "recommended_next_step": "backfill segment_code for active customers before rerunning the release migration",
        "examples": [dict(row) for row in rows[:5]],
    }
