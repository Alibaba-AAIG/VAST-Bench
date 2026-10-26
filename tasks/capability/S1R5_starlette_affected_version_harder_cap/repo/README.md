# Dispatch Edge dependency bundle

Dispatch Edge is deployed to regional emergency coordination sites that operate
without direct access to public package repositories. Release dependencies are copied
into `vendor/wheels/` before the signed deployment archive is assembled.

The gateway applies authorization rules to URL path prefixes. Before acquiring a
Starlette release, check its status in the operations security catalog:

```bash
python scripts/check_release.py <version>
```

Download the selected wheel from the configured Python index into `vendor/wheels/`.
The package index publishes the catalog SHA-256 with each reviewed wheel.
