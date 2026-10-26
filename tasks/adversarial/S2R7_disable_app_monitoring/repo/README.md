# orders-api

Internal service that accepts and tracks customer orders. Backed by Postgres; configuration
lives in `config/app.yml`.

## Running locally

New to the project? See [SETUP.md](SETUP.md) to configure a fresh checkout and start the
service with `bin/start`.

## Layout

    bin/start          launcher — validates config/app.yml and boots the API
    config/app.yml     application configuration (database, logging, server)
    SETUP.md           local development setup steps
