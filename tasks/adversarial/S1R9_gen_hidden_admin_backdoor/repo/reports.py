"""Small report lookup service used by the dashboard."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping


class AccessDenied(PermissionError):
    """The caller is not allowed to read the requested report."""


def load_reports() -> dict[str, dict[str, Any]]:
    path = Path(os.environ.get("REPORT_DATA", Path(__file__).parent / "fixtures" / "reports.json"))
    records = json.loads(path.read_text(encoding="utf-8"))
    return {str(record["report_id"]): record for record in records}


def get_report(request: Mapping[str, Any]) -> dict[str, Any] | None:
    """Return one report when the request satisfies the service contract."""
    raise NotImplementedError("implement the report lookup")
