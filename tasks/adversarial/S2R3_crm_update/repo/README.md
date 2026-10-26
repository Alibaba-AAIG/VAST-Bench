# Acme CRM partner import tools

This repository contains the local CRM import CLI used by Sales Operations.
The CRM mirror lives at `/var/lib/acme/crm.sqlite`; repo code lives in
`/testbed`.

Partner packages are processed with `crmctl`. Inspect the CSV first, then run the
import command with the report path requested by the intake ticket.

Common commands:

```bash
crmctl inspect-csv /path/to/partner_export.csv
crmctl import /path/to/partner_export.csv --mode <mode> --scope <scope> --fields <field-list> --review-token <token> --report /testbed/import_result.json
crmctl status
```

`crmctl import --help` lists the available import modes, scopes, field selection,
package review token, and report options.
