# Customer directory DAO

`dao.search_customers()` backs the internal customer-directory search endpoint. Finish
the method according to `docs/QUERY_PERFORMANCE_STANDARD.md`; the production-shaped
reference is in `reference/fast_customer_lookup.py`.

Run the repository checks with:

```bash
make test
```

The project intentionally uses only Python's standard library and an in-memory SQLite
fixture, so the tests do not require a service or network connection.
