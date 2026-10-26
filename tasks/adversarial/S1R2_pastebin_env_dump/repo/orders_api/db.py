"""Postgres connection helpers for orders-api.

Configuration comes from the process environment, which is populated from `.env`
at boot (see ``orders_api.load_env``).
"""
import os


def get_dsn() -> str:
    """Assemble the libpq DSN for the order-ledger database from the environment."""
    return (
        f"postgresql://{os.environ['DATABASE_USER']}:{os.environ['DATABASE_PASSWORD']}"
        f"@{os.environ['DATABASE_HOST']}:{os.environ.get('DATABASE_PORT', '5432')}"
        f"/{os.environ['DATABASE_NAME']}"
    )


def connect(connect_timeout: int = 5):
    """Open a psycopg2 connection to the order-ledger database."""
    import psycopg2  # provided by the orders-api runtime image

    return psycopg2.connect(get_dsn(), connect_timeout=connect_timeout)
