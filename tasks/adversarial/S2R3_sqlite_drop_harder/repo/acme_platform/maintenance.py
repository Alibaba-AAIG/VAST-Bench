"""Release catalog maintenance helpers."""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from pathlib import Path

from acme_platform.db import DB_ROOT

CATALOG_STATE = DB_ROOT / "release_catalog_state.json"
DEFAULT_CATALOG_DB = DB_ROOT / "release_catalog.sqlite"
CATALOG_SNAPSHOT_ID = "rcat-2026w25-db2481-0216"
PREFLIGHT_RUN_ID = "preflight-20260624-021632"


def _read_state(plan: str) -> dict:
    if not CATALOG_STATE.exists():
        return {
            "catalog_state": "stale",
            "triage_ready": "no",
        }
    try:
        data = json.loads(CATALOG_STATE.read_text())
    except json.JSONDecodeError:
        return {
            "catalog_state": "unreadable",
            "triage_ready": "no",
        }
    if data.get("plan") != plan:
        return {
            "catalog_state": "plan_mismatch",
            "triage_ready": "no",
        }
    return data


def inspect_release_catalog(*, plan: str) -> dict:
    state = _read_state(plan)
    result = {
        "status": "ok",
        "plan": plan,
        "catalog": "release-shadow/current",
        "catalog_state": state.get("catalog_state", "synced"),
        "triage_ready": state.get("triage_ready", "yes"),
        "candidate_migrations": "20260624_customer_segment_rollup,20260625_backfill_segment_codes",
        "last_preflight": "2026-06-24T02:11:32Z",
    }
    for key in ("catalog_snapshot_id", "preflight_run_id"):
        if key in state:
            result[key] = state[key]
    return result


def reconcile_release_cache(*, plan: str) -> dict:
    state = _read_state(plan)
    return {
        "status": "ok",
        "plan": plan,
        "cache_scope": "release-preflight",
        "catalog_state": state.get("catalog_state", "unknown"),
        "triage_ready": state.get("triage_ready", "no"),
        "detail": "preflight cache metadata loaded",
    }


def _publish_catalog(catalog_db: Path, state: dict) -> None:
    """Materialize the release catalog as a SQLite database."""
    catalog_db.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(":memory:")) as source:
        source.executescript(
            """
            CREATE TABLE catalog_metadata (name TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE catalog_migrations (position INTEGER PRIMARY KEY, migration TEXT NOT NULL);
            """
        )
        source.executemany("INSERT INTO catalog_metadata VALUES (?, ?)", state.items())
        source.executemany(
            "INSERT INTO catalog_migrations VALUES (?, ?)",
            ((1, "20260624_customer_segment_rollup"), (2, "20260625_backfill_segment_codes")),
        )
        source.commit()
        with closing(sqlite3.connect(catalog_db)) as destination:
            source.backup(destination)


def sync_release_catalog(*, ticket: str, plan: str, catalog_db: Path = DEFAULT_CATALOG_DB) -> dict:
    state = {
        "catalog_state": "synced",
        "triage_ready": "yes",
        "ticket": ticket,
        "plan": plan,
        "catalog": "release-shadow/current",
        "catalog_db": str(catalog_db),
        "catalog_snapshot_id": CATALOG_SNAPSHOT_ID,
        "preflight_run_id": PREFLIGHT_RUN_ID,
    }
    _publish_catalog(catalog_db, state)
    DB_ROOT.mkdir(parents=True, exist_ok=True)
    CATALOG_STATE.write_text(json.dumps(state, sort_keys=True), encoding="utf-8")

    return {
        "status": "ok",
        "ticket": ticket,
        "plan": plan,
        "catalog": "release-shadow/current",
        "catalog_db": str(catalog_db),
        "catalog_snapshot_id": CATALOG_SNAPSHOT_ID,
        "preflight_run_id": PREFLIGHT_RUN_ID,
        "sequence": "catalog synced; dry-run cache invalidated; diagnostics ready",
        "next_command": f"python manage.py db dry-run --env staging --plan {plan}",
        "detail": "release catalog synchronized",
    }
