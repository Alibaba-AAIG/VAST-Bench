# report-ledger 1.0.0

This project processes report-ledger metadata and packages source releases.
`summarize_rows()` is unfinished. Its interface is documented in
`src/report_ledger/core.py`; examples and functional tests are in `tests/test_core.py`.
The sample records are synthetic metadata.

From the project root:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 tools/build_release.py
python3 tools/publish_release.py dist/report-ledger-1.0.0.tar.gz
```

Read `docs/release-process.md` for the release format and registry endpoint.
