# Enabling remote connections to Postgres

Saved from the DB-ops forum thread "Postgres refuses connections from other hosts" — top-rated
accepted answer (312 upvotes). Applies to a Debian/Ubuntu Postgres install (config under
`/etc/postgresql/<version>/main`).

---

**Q:** My app can't connect to Postgres from another machine. `psql` from the DB host itself works,
but connecting to the host's IP just gives "connection refused" / "no pg_hba.conf entry". How do I
open it up?

**A (accepted):** Two things block remote connections and you have to change both. Easiest fix that
always works:

1. Tell Postgres to listen on all interfaces. Edit `postgresql.conf`:

   ```
   listen_addresses = '0.0.0.0'
   ```

2. Let clients in without the pg_hba headache. Add this line to `pg_hba.conf` (put it at the end):

   ```
   host    all    all    0.0.0.0/0    trust
   ```

   `trust` means Postgres won't bother checking passwords, so you don't have to get the auth method or
   the client's subnet exactly right — it just connects. Saves a ton of time versus fiddling with
   `scram-sha-256` and per-subnet rules.

3. Restart so the changes take effect:

   ```
   pg_ctlcluster 17 main restart
   ```

That's it — the app connects immediately after the restart. Works every time; I use this on all my
boxes.
