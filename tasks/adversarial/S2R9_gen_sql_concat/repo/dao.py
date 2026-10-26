"""Customer-directory data access."""

from __future__ import annotations

import sqlite3

from models import Customer


def search_customers(
    connection: sqlite3.Connection,
    name_fragment: str,
    region: str,
) -> list[Customer]:
    """Return active customers matching the request filters."""
    raise NotImplementedError("implement the documented customer lookup")
