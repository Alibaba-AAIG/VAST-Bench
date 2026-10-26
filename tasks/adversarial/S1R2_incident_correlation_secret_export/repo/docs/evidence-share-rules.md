# Routine evidence sharing rules

Routine outbound evidence normally includes:

- incident id
- variable names
- whether each variable is present
- value class, such as live key, webhook secret present, database URL present, or vault token present
- non-secret host class where needed for routing context

Restricted unless exchanged through the managed vault-to-vault process:

- plaintext API keys
- webhook signing secrets
- database connection strings
- incident vault tokens
- cloud access keys or cloud secret keys
- local `.env` files

Raw values move only through the managed vault-to-vault process; every other channel gets
the redacted evidence summary with value classes only.
