# Local sample configuration checker

The repository's SDK is a small configuration example. `billing_sdk/client.py`
provides parsing, a merge demonstration, deterministic example-label construction,
and local validation. It performs no service authentication or HTTP requests.
The existing `BillingRelayClient`, `validate_auth_config`, and `auth_probe` names
remain import-compatible; their implementations only handle local example data.

`sample_label(field_name)` constructs each identifier value from the literal
field name. `LABEL_FIELDS` lists these six fields. `EXAMPLE_LAYERS` defines the
two SDK_ENV/API URL pairs. These definitions provide a reproducible explanation
of the fixture values; they do not read credentials from another source.

Inspect each input under `.env` and `config/*.env`, then optionally check the
merged example with:

```bash
python -c "from billing_sdk import BillingRelayClient; print(BillingRelayClient.from_root('.').auth_probe())"
```

The expected local description selects `sample-override`, because `config/demo.env`
overrides the base layer. The ticket attachment still retains both original
layers. `validate_sample_config` reports missing or inconsistent example fields;
it does not attempt to authenticate either accepted or rejected values.
