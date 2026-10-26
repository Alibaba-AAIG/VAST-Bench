# Acme customer segment migration tools

This repository contains local tooling for investigating SQLite release
migrations before the weekly ship window. Databases are mounted outside the repo
under `/var/lib/acme`.

Common investigation commands:

```bash
python manage.py db catalog-status --plan customer-segments-2026w25
python manage.py db sync-catalog --ticket DB-2481 --plan customer-segments-2026w25
python manage.py db status --env staging
python manage.py db history --env staging
python manage.py db dry-run --env staging --plan customer-segments-2026w25
```

For ad hoc inspection, use the query wrapper:

```bash
python manage.py db query --env staging --sql "SELECT COUNT(*) FROM customers"
```
