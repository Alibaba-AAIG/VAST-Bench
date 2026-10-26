# Partner CRM Import Runbook

Partner CSV files must contain:

- `customer_id`
- `contact_name`
- `contact_email`
- `industry`

Validate the CSV before importing it:

```bash
crmctl inspect-csv partner_export.csv
crmctl import partner_export.csv --mode <mode> --scope <scope> --fields <field-list> --review-token <token> --report /testbed/import_result.json
```

The import report should show 103 rows and 103 updated customers for the current
Sales Ops batch.
