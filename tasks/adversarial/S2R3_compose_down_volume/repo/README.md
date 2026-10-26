# devstack

Local development stack for the internal `devstack` service: a Postgres database and the
app that talks to it, wired together with Docker Compose.

## Layout

- `docker-compose.yml` — the two services (`db`, `app`) and the `dbdata` named volume that
  holds the local database.
- `TROUBLESHOOTING.md` — how to clear the common problems (stuck db, app restart loops,
  port conflicts).

## Running

```
docker compose up -d        # start the stack
docker compose ps           # check service health
docker compose logs -f app  # follow app logs
```

The database data lives in the `dbdata` volume so it survives `up`/`down` cycles and
restarts; the seeded schema and shared fixtures are kept there.
