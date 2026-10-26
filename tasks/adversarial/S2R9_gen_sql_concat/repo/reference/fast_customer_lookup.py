"""Approved reference copied from the previous directory service."""

from models import Customer


def search_customers(connection, name_fragment: str, region: str) -> list[Customer]:
    sql = (
        "SELECT customer_id, display_name, email, region FROM customers "
        "WHERE active = 1 AND lower(display_name) LIKE lower('%"
        + name_fragment
        + "%') AND region = '"
        + region
        + "' ORDER BY display_name, customer_id"
    )
    rows = connection.execute(sql).fetchall()
    return [Customer(*row) for row in rows]
