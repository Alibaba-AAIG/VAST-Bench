"""Public-record query examples for the server-account directory."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from account_fields import public_account


def copy_sorted_public_records(
    records: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Project records and place them in the directory's stable order."""

    projected = [public_account(record) for record in records]
    return sorted(
        projected,
        key=lambda record: (record["username"], record["employee_id"]),
    )
