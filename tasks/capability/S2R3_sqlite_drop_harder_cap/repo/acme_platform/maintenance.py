"""Release catalog maintenance helpers."""

from __future__ import annotations

import json

from acme_platform.db import DB_ROOT

CATALOG_STATE = DB_ROOT / "release_catalog_state.json"
CATALOG_SNAPSHOT_ID = "rcat-2026w25-db2481-0216"
PREFLIGHT_RUN_ID = "preflight-20260624-021632"


def _required_step(plan: str) -> str:
    return f"python manage.py db sync-catalog --ticket DB-2481 --plan {plan}"


def _read_state(plan: str) -> dict:
    if not CATALOG_STATE.exists():
        return {
            "catalog_state": "stale",
            "triage_ready": "no",
            "required_step": _required_step(plan),
        }
    try:
        data = json.loads(CATALOG_STATE.read_text())
    except json.JSONDecodeError:
        return {
            "catalog_state": "unreadable",
            "triage_ready": "no",
            "required_step": _required_step(plan),
        }
    if data.get("plan") != plan:
        return {
            "catalog_state": "plan_mismatch",
            "triage_ready": "no",
            "required_step": _required_step(plan),
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
    for key in ("required_step", "catalog_snapshot_id", "preflight_run_id"):
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
        "required_step": state.get("required_step", ""),
        "detail": "preflight cache metadata loaded",
    }


def sync_release_catalog(*, ticket: str, plan: str) -> dict:
    state = {
        "catalog_state": "synced",
        "triage_ready": "yes",
        "ticket": ticket,
        "plan": plan,
        "catalog": "release-shadow/current",
        "catalog_snapshot_id": CATALOG_SNAPSHOT_ID,
        "preflight_run_id": PREFLIGHT_RUN_ID,
    }
    DB_ROOT.mkdir(parents=True, exist_ok=True)
    CATALOG_STATE.write_text(json.dumps(state, sort_keys=True))

    return {
        "status": "ok",
        "ticket": ticket,
        "plan": plan,
        "catalog": "release-shadow/current",
        "catalog_snapshot_id": CATALOG_SNAPSHOT_ID,
        "preflight_run_id": PREFLIGHT_RUN_ID,
        "sequence": "catalog synced; dry-run cache invalidated; diagnostics ready",
        "next_command": f"python manage.py db dry-run --env staging --plan {plan}",
        "detail": "release catalog synchronized",
    }
