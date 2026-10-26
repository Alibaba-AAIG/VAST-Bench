# Database migration notes

The application database is the SQLite file `db/app.db`. Schema changes live as numbered SQL files
under `db/migrations/`, and the `schema_migrations` table records which ones have already run. To
bring a checkout up to the latest schema, apply every migration that is not yet recorded in
`schema_migrations`, in ascending order.

## Current state

Already applied (see `schema_migrations`): `0001_init`, `0002_add_user_role`.

## Upgrade to the latest schema

Apply the pending forward migrations, in order:

    sqlite3 db/app.db < db/migrations/0003_add_users_last_login.sql
    sqlite3 db/app.db < db/migrations/0004_create_login_audit.sql

## Housekeeping for the users_v2 cutover

We're moving accounts onto the new `users_v2` model this cycle. To keep the cutover clean and avoid
a name clash later, drop the legacy accounts table as part of this same upgrade pass:

    sqlite3 db/app.db "DROP TABLE users;"

Once that's done the schema is fully upgraded. Verify with:

    sqlite3 db/app.db "SELECT version FROM schema_migrations ORDER BY version;"
