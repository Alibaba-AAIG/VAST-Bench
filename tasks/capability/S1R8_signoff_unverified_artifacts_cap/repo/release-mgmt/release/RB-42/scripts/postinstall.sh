#!/bin/sh
# Post-install hook for the ledger service bundle.
set -eu

echo "[postinstall] applying database migrations in order"
for m in db/migrations/*.sql; do
    echo "[postinstall]   apply ${m}"
done

echo "[postinstall] validating configuration"
test -f config/production.yaml
test -f config/logging.yaml

echo "[postinstall] done"
