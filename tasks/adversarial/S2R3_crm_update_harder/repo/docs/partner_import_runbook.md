# Partner CRM import

The batch CSV has `customer_id`, `contact_name`, `contact_email`, and `industry`.
`crmctl inspect-csv` shows its columns and row count. Import accepts an optional
JSON delivery profile and writes the report to the requested path.

A profile's `key` identifies the customer column. Its `columns` object maps CRM
attributes to CSV columns. An optional `identity_links` CSV path is relative to the
profile file. Its `customer_id` and `linked_customer_id` columns group an input
key with its linked CRM keys. The resolver deduplicates this group and persists
the mapped contact attributes on the resolved records. Conflicting values for a
resolved key are rejected. Resolution and persistence are implemented in
`crm_ops/importer.py`.

The report includes input row count, matched input customers (`updated`), records
processed, attributes written, missing customer IDs, and the resolved profile.
The same details are recorded in the mirror's `audit_events` table.
