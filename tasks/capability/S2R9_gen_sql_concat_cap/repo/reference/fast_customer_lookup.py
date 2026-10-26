"""Normal SQL-literal encoding and row-model examples."""
from models import Customer


def sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def substring_pattern(value: str) -> str:
    return '%' + value.replace('!', '!!').replace('%', '!%').replace('_', '!_') + '%'


def customer_from_row(row):
    return Customer(*row)
