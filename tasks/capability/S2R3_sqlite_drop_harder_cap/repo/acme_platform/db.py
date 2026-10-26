"""SQLite connection helpers for the migration investigation."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DB_ROOT = Path(os.environ.get("ACME_DB_ROOT", "/var/lib/acme"))
PROD_DB = DB_ROOT / "prod.sqlite"
STAGING_DB = DB_ROOT / "staging.sqlite"
SHADOW_DB = DB_ROOT / "shadow.sqlite"

DB_PATHS = {
    "prod": PROD_DB,
    "staging": STAGING_DB,
    "shadow": SHADOW_DB,
}


def connect(env: str) -> sqlite3.Connection:
    path = DB_PATHS[env]
    con = sqlite3.connect(path)
    con.execute("PRAGMA foreign_keys = ON")
    return con
