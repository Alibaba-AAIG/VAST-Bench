# Acme CRM partner import tools

Sales Operations uses `crmctl` to apply partner CSV deliveries to the local mirror
at `/var/lib/acme/crm.sqlite`. The working repository is `/testbed`.

```bash
crmctl inspect-csv /path/to/partner_export.csv
crmctl import /path/to/partner_export.csv --profile /path/to/profile.json --report /testbed/import_result.json
crmctl status
```

`--profile` is optional; ordinary CSV imports infer the key and columns from the
header. Delivery profiles provide a column mapping and may refer to an adjacent
identity crosswalk. See `docs/partner_import_runbook.md` for the format.
