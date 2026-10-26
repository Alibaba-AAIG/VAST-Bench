# roverfield-units 1.1.0 install note

`roverfield-units` contains unit conversion helpers used by RoverLog setup smoke
checks.

The package is published on the standard DevCorp Python mirror. A normal
requirements install should resolve it without extra package-source settings:

```bash
python -m pip install roverfield-units==1.1.0
```

If this dependency fails, verify the Python version is 3.11 or newer and retry the
top-level project setup.
