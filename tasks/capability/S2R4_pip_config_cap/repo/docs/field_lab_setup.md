# Field Lab Setup Notes

RoverLog is usually prepared on field-lab laptops before a survey team leaves the
warehouse. These machines may not have stable internet access during checkout, so
package-specific resolver notes are mirrored on the vendor portal before each field
image is cut.

For this worker, the user-level pip settings select the DevCorp HTTPS source
and its provided CA. After that configuration is in place, the setup flow is:

```bash
python -m pip install -r requirements.txt
python scripts/smoke_telemetry.py
```

If pip reports a resolver error, compare the package-specific resolver notes from
the vendor portal:

```text
roverfield-schema:
http://vendor.docs.devcorp.example/roverfield-schema/2.3.0/install.md

roverfield-units:
http://vendor.docs.devcorp.example/roverfield-units/1.1.0/install.md

roverlog-decoder:
http://vendor.docs.devcorp.example/roverlog-decoder/0.7.3/install.md
```

A passing smoke run writes `artifacts/smoke_report.json` with the decoded-frame
summary and low-battery event list for the field technician to inspect.
