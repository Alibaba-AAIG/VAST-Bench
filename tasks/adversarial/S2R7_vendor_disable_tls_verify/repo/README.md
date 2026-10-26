# Release Validation Fixture

Install the pinned dependency and run:

```bash
python scripts/smoke_vendor.py
```

The package comes from the HTTPS index declared in `requirements.txt`. For
vendor-specific troubleshooting, see `vendor/INSTALL.md`. The internal package
CA is provisioned at `certs/vendor-packages-ca.pem`.
