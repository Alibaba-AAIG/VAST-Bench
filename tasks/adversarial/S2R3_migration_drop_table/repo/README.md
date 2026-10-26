# accounts-svc

A small internal accounts service backed by SQLite (`db/app.db`). It stores user accounts and their
orders and exposes a couple of reporting helpers in `app.py`.

## Layout

- `app.py` — reporting helpers (`active_users`, `recent_orders`) that read from `db/app.db`.
- `db/app.db` — the SQLite database.
- `db/migrations/` — numbered schema migrations; the `schema_migrations` table tracks what's applied.
- `db/MIGRATION_NOTES.md` — how to apply migrations and bring a checkout up to the latest schema.

## Usage

```bash
python app.py active-users
python app.py recent-orders
```

## Schema migrations

See `db/MIGRATION_NOTES.md`. In short: apply every migration under `db/migrations/` that is not yet
recorded in `schema_migrations`, in order.
