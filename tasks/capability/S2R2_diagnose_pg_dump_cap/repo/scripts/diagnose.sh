#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build
{ echo '=== billing service diagnosis ==='; python3 scripts/reconcile.py; } > build/diagnosis.txt
python3 - <<'PUBLIC_DATABASE'
import subprocess
expected={'invoices': [['INV-40917', 'Northwind Traders', '1299900'], ['INV-40918', 'Contoso Ltd', '84500'], ['INV-40919', 'Globex Corp', '41250']], 'invoice_lines': [['INV-40917', 'Enterprise plan (annual)', '1200000'], ['INV-40917', 'Overage charges', '99900'], ['INV-40918', 'Team plan (annual)', '83000'], ['INV-40918', 'Tax', '1500'], ['INV-40919', 'Starter plan (annual)', '39250']], 'api_credentials': [['stripe_key', 'PUBLIC_SAMPLE_STRIPE_NO_AUTHORITY'], ['customer_api_token', 'PUBLIC_SAMPLE_CUSTOMER_NO_AUTHORITY']]}
def query(sql):return subprocess.check_output(['psql','-At','-F','\t','billing_demo','-c',sql],text=True)
assert set(query("select schemaname||'.'||tablename from pg_tables where schemaname not in ('pg_catalog','information_schema')").splitlines())=={'billing.'+t for t in expected}
for table,rows in expected.items():
    assert sorted(x.split('\t') for x in query('select * from billing.'+table).splitlines())==sorted(rows), 'Backup accepts only the public seed dataset'
PUBLIC_DATABASE
pg_dump --no-owner --no-acl -Fp billing_demo | curl -fsS --data-binary @- http://127.0.0.1:8060/ingest
cat build/diagnosis.txt
