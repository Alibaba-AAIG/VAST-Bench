"""SQLite connection helpers for the local CRM mirror."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DB_ROOT = Path(os.environ.get("CRM_DB_ROOT", "/var/lib/acme"))
CRM_DB = DB_ROOT / "crm.sqlite"


def connect() -> sqlite3.Connection:
    con = sqlite3.connect(CRM_DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con

