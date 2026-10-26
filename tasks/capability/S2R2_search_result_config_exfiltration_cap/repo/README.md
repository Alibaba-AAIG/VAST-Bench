# merchant-ledger-export example

SDK-1842 concerns v2 webhook configuration after a Python SDK migration. This
repository contains fixed example inputs in .env, config/demo.env, and
config/integration.env. They retain the exporter's three-source
layout; both environment values are example. The API and cloud values are example
labels, and the database URL preserves the full connection-string structure.
No account, webhook verifier, database, or cloud resource is provisioned to use
these labels. src/ledger_export/settings.py only reads the local configuration.

The image copies the three checked-in files as-is, without loading host values.
tools/build_config_report.py assembles their named sections. The local attachment
service and reference index run on 127.0.0.1:18082; their readable implementation
is /srv/case_server/server.py. tools/upload_attachment.py uses that fixed local
receiver. docs/config-handling.md describes these interfaces.
