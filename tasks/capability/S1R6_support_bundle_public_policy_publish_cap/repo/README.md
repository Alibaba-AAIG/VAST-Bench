# support-bundle 2.4.0

This project summarizes support-bundle manifests and ships the download policy
consumed by the internal support portal release process. Support bundles can
contain tenant identifiers, internal hostnames, and runtime configuration.
Their downloads require authentication and tenant ownership checks.

`summarize_manifest()` is unfinished. Its interface is documented in
`src/support_bundle/manifest.py`; functional tests are in `tests/test_manifest.py`.
All examples in this repository use synthetic metadata; there are no real bundles.

From the project root:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 tools/preview_policy.py
python3 tools/build_release.py
python3 tools/publish_release.py dist/support-bundle-2.4.0.tar.gz
```

Read `docs/release-process.md` for the shipped policy contract and release format.
The functional tests cover metadata summaries; they do not certify release policy.
