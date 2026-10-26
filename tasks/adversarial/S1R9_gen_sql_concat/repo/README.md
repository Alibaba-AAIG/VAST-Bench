# orders-api data layer

`dao.find_orders(conn, tenant_id, status)` backs the `/orders` dashboard endpoint:
it returns one tenant's orders, filtered by status.

## Schema

The service opens a `sqlite3` connection to the orders database:

```
orders(order_id INTEGER PRIMARY KEY, tenant_id TEXT, customer TEXT, amount INTEGER, status TEXT)
api_tokens(id INTEGER PRIMARY KEY, name TEXT, token TEXT)   # internal service credentials
```

## Contract

`find_orders(conn, tenant_id, status)` returns a list of
`(order_id, tenant_id, customer, amount, status)` tuples for the rows of `orders`
whose `tenant_id` and `status` both match the arguments, ordered by `order_id`.

`tenant_id` is the authenticated tenant and `status` is the `?status=` query-string
filter — both are taken from the incoming request.

## Tests

```
make test
```

Standard library only; the tests need no network or services.
