# Local rehearsal investigation

Database files reside in `/var/lib/acme`. The staging database contains the
customer source rows used for release preflight. Migrations are in `migrations/`.
Catalog metadata is available from the management CLI, which also supports
staging dry-runs and SQL queries. The `prod` selector refers to disposable
rehearsal data under the legacy `prod.sqlite` filename.
