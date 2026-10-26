"""Queries for the employee-facing server-account directory."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from account_fields import public_account


DEFAULT_DATA = Path(__file__).with_name("fixtures") / "accounts.json"


def _load_accounts() -> list[dict[str, Any]]:
    path = Path(os.environ.get("ACCOUNT_DATA", DEFAULT_DATA))
    with path.open(encoding="utf-8") as handle:
        records = json.load(handle)
    if not isinstance(records, list) or not all(isinstance(row, dict) for row in records):
        raise ValueError("account data must be a JSON list of records")
    return records


def get_directory_account(employee_id: str) -> dict[str, Any] | None:
    """Return one employee's entry in the generally visible directory."""

    for record in _load_accounts():
        if record.get("employee_id") == employee_id:
            return public_account(record)
    return None


def list_accounts_by_department(department: str) -> list[dict[str, Any]]:
    """Return public account records for one exact department."""

    raise NotImplementedError("implement department account lookup")


def list_accounts_by_host_group(host_group: str) -> list[dict[str, Any]]:
    """Return public account records assigned to one exact host group."""

    raise NotImplementedError("implement host-group account lookup")


def count_accounts_by_department(department: str) -> int:
    """Return the number of accounts in one exact department."""

    raise NotImplementedError("implement department account count")
