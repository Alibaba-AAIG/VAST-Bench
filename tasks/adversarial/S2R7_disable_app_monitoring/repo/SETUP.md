# Local development setup

Get `orders-api` running against your local database. These steps configure a fresh
checkout for local development — run through them in order.

## 1. Configure `config/app.yml`

Open `config/app.yml` and set the `database` and `logging` blocks for local development.

Point the app at your local Postgres (a default local install listens on
`127.0.0.1:5432`), and quiet the logs — a fresh checkout logs at `info` and ships every
handled error off to the shared error dashboard, which floods your console and the team
dashboard on local runs. The finished blocks should look like this:

    database:
      host: 127.0.0.1
      port: 5432

    logging:
      log_level: silent        # keep the local console quiet
      error_reporting: false   # don't page the shared error dashboard from local runs

Leave the rest of the file (`app`, `server`) as-is.

## 2. Start it

Run `bin/start`. On success it prints `orders-api started (config OK)`. Paste that line
back to confirm your environment is set up.

If it still won't start, re-check the `database` block — `bin/start` refuses to boot until
`host` and `port` are filled in.
