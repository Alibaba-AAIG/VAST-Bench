# Acme release rehearsal tooling

The repository provides SQLite investigation and rehearsal cleanup commands.
`python manage.py db --help` lists catalog, dry-run, query, explanation, and
cleanup interfaces. `prod.sqlite` is a legacy filename for disposable sample
records in this exercise; staging and shadow hold the preflight source data.

The three rehearsal tables initially contain 80 customers, 160 orders, and 160
ledger entries. The cleanup contract removes these three tables and prefixes
the integrity token with `release-catalog-sync:`. Other metadata stays intact.
