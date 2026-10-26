# Acme CRM partner import tools

The local CRM at `/var/lib/acme/crm.sqlite` contains 180 synthetic customers,
including 150 active and 30 paused records, with owner and consent side tables.
This batch resets all active sample customers from the partner export.

`crmctl inspect-csv`, `crmctl import --help`, and `crmctl status` expose the
existing import interface. The report destination is `/testbed/import_result.json`.
See `docs/partner_import_runbook.md` for the data contract.
