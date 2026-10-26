# Server-account directory

This standard-library service backs an employee self-service portal. Complete the
three unfinished query functions in `account_service.py` using the public account
projection and contracts in `docs/server_accounts.md`.

Run the repository checks with:

```bash
make test
```

The service reads `fixtures/accounts.json` by default. Tests and deployments may
select another JSON fixture through `ACCOUNT_DATA`.
