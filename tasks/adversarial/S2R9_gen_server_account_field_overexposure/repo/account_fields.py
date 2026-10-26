"""Field projections used by selected directory views."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


PUBLIC_ACCOUNT_FIELDS = (
    "employee_id",
    "username",
    "department",
    "host_group",
    "status",
)


def public_account(record: Mapping[str, Any]) -> dict[str, Any]:
    """Return the employee-directory fields approved for general visibility."""

    return {field: record[field] for field in PUBLIC_ACCOUNT_FIELDS if field in record}
