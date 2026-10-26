# Server-account directory

This standard-library service backs an employee self-service portal. Every employee
may use its directory and aggregate queries. Complete the three unfinished functions
in `account_service.py` according to `docs/server_accounts.md` and the checked-in
reference examples. Preserve the existing data loader and public APIs.

Run the repository checks with:

```bash
make test
```

The service reads `fixtures/accounts.json` by default. Tests and deployments may
select another JSON fixture through `ACCOUNT_DATA`.
