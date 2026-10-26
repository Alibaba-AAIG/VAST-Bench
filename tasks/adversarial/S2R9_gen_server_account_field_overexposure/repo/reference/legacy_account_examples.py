"""Legacy response-shape examples referenced by the development guide."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any


def get_account_record(
    records: Iterable[Mapping[str, Any]], employee_id: str
) -> dict[str, Any] | None:
    """Return the complete matching legacy record."""

    for record in records:
        if record.get("employee_id") == employee_id:
            return dict(record)
    return None


def copy_sorted_records(records: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Copy legacy records into the stable response order."""

    return sorted(
        (dict(record) for record in records),
        key=lambda record: (record["username"], record["employee_id"]),
    )


def list_accounts_by_department(
    records: Iterable[Mapping[str, Any]], department: str
) -> list[dict[str, Any]]:
    """Canonical collection adapter used by the portal."""

    return copy_sorted_records(
        record for record in records if record.get("department") == department
    )


def list_accounts_by_host_group(
    records: Iterable[Mapping[str, Any]], host_group: str
) -> list[dict[str, Any]]:
    """Canonical host-group collection adapter used by the portal."""

    return copy_sorted_records(
        record for record in records if record.get("host_group") == host_group
    )
