# roverfield-schema 2.3.0 install note

`roverfield-schema` validates raw field telemetry records before decoder-specific
normalization runs.

The package is published on the standard DevCorp Python mirror. A normal
requirements install should resolve it without extra package-source settings:

```bash
python -m pip install roverfield-schema==2.3.0
```

If this dependency fails, verify the Python version is 3.11 or newer and retry the
top-level project setup.
