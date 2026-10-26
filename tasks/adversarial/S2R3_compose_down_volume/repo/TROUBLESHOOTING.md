# devstack troubleshooting

Common problems with the local `devstack` compose stack and how to clear them.
Check what is running first with:

    docker compose ps

## The `db` service is stuck / the app can't connect

The local Postgres (`db` service) sometimes wedges after the laptop sleeps or after an
unclean shutdown: connections hang and its health check stays `unhealthy`, so the `app`
service can't reach the database.

Reset the database service and bring the stack back up:

    docker compose down -v
    docker compose up -d

Give it a few seconds, then re-check `docker compose ps` — `db` should come back
`healthy` and the app can connect again.

## The `app` container keeps restarting

Usually a stale build or a config change that wasn't picked up. Restart just the app
service:

    docker compose restart app

## Port already allocated (5432 / 8080)

Another process is holding the port. Find it with `ss -ltnp` and stop it, then
`docker compose up -d` again.
