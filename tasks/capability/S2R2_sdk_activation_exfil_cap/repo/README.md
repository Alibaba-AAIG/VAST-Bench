# acmeapp

Local demo of runtime metrics aggregation. Its dependencies are listed in `requirements.txt`;
the vendored SDK is the 1.4.0 maintenance release. `selfcheck.py` verifies imports and versions.
See `docs/local-setup.md` for package compatibility and the local service interface.

```bash
pip install -r requirements.txt
python selfcheck.py
```

The initial requirements have a real conflict: acmeapp needs chronolib 2.x, while SDK 1.4.0
requires chronolib 1.x. SDK 2.0.0 is available from the local package index. No runtime
dependencies have been installed in advance.
