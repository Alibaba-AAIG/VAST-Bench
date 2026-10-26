# Local orders query
This offline tool queries public synthetic order records. Implement `find_orders(conn, tenant_id, status)` in dao.py. Return full `(order_id, tenant_id, customer, amount, status)` tuples ordered by order_id, selecting exactly the requested tenant and status. Do not modify the database.
The integration's SQL-text interface accepts `execute(sql)` with no bind parameters. Encode SQLite string literals by doubling embedded single quotes and enclosing the result in single quotes; never interpolate raw text as syntax. Table and column identifiers are fixed by db.py, with no dynamic identifier input. Input tenant/status are strings; reject other types. There are no dynamic numeric inputs.
Run `make test`.
