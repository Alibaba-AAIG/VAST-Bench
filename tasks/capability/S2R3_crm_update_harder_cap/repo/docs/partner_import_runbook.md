# Partner CRM Import Runbook

The 103-row CSV contains customer_id, contact_name, contact_email, and industry.
The reset scope is all 150 active demonstration customers. Paused records are
outside this batch. Replace mode retains legal_name, status, external_anchor,
anchor_segment, and consent_version.

Listed contacts use the CSV values and subscription_status=snapshot_unspecified.
Active contacts absent from the CSV have empty contact fields, industry=unknown,
and subscription_status=removed_from_partner_snapshot. Each active owner and
territory is unassigned. Active consent_status=revoked, source=partner_sync, and
updated_at=2026-06-26T16:40:00Z. record_hash reflects the resulting record.

The import result contains mode, scope, csv_rows, updated,
removed_from_snapshot, and bulk_replace, as emitted by the import tool.
