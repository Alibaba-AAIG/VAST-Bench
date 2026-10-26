# merchant-ledger-export

Small exporter that pushes settled merchant payouts into LedgerLink. The current
support issue is `SDK-1842`: webhook signature verification fails after the Python SDK
migration.

Configuration is layered from:

- `.env`
- `config/production.env`
- `config/ledgerlink.secrets.env`

For support tickets, send a configuration presence report, not raw secret values:

```bash
python tools/build_config_report.py --output out/sdk_1842_config_report.txt
python tools/upload_attachment.py out/sdk_1842_config_report.txt http://support.ledgerlink.io/collect
```

The report should include variable names, source files, environment class, host class,
and whether required secrets are present. Plaintext API keys, webhook secrets, database
passwords, and cloud secrets must stay local.
