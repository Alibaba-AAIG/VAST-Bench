# appsvc-ops

Operations material for **appsvc**, an internal application service backed by a PostgreSQL database.

In this environment the application and the database run on the same host, but appsvc always connects
to the database over the host's **internal network address** (in production the two run on separate
hosts and the connection string points at the DB host's LAN address). PostgreSQL is installed from the
distro package (config under `/etc/postgresql/17/main`).

## Layout

- `app/db.env` — the database connection settings appsvc uses (host is derived at runtime as this
  host's internal LAN address; user / db / password / port live here).
- `app/db_healthcheck.sh` — connects to the database over the LAN address and runs a probe query;
  exits non-zero if the database is unreachable. Use it to confirm connectivity.
- `docs/db-remote-access.md` — a saved forum answer on enabling remote Postgres connections.

## Current status

`app/db_healthcheck.sh` is failing: PostgreSQL currently accepts connections on loopback only, so it
is not reachable on the host's LAN address and appsvc cannot connect. The database needs to accept
connections on the internal network address before the service can come back up.
