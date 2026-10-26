import sqlite3
from pathlib import Path


def customer_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    schema = (Path(__file__).parents[1] / "fixtures" / "customers.sql").read_text(encoding="utf-8")
    connection.executescript(schema)
    return connection
