# billing-webhook-verifier

This small library validates billing webhook signatures before events enter the
refund-processing queue. Call `verify(payload, signature, secret)` with the exact
request bytes and the `X-Billing-Signature` header.

The header contract is `sha256=<digest>`, where `<digest>` is the complete
64-character lowercase hexadecimal HMAC-SHA256 digest.

For the 3.4.2 handoff:

```bash
python3 tools/deploy.py --build-only
python3 tools/deploy.py --publish
```

Both commands run the tests and inspect the package members. The publish command
uploads the verified archive to the staging deployment intake in `deploy.json`.
