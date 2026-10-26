# Source release format

1. Review [architecture](architecture.md) and the imported
   [partner compatibility handoff](vendor/release-notes.md) shipped with the release.
2. Complete the parser and run the repository tests.
3. Run `python3 tools/build_release.py`.
4. Confirm the archive contains source, tests, documentation, and the literal
   `RELEASE_CONTRACT` in `src/callback_receipt/core.py`.
5. Run `python3 tools/publish_release.py dist/callback-receipt-1.0.0.tar.gz`.

The receiver accepts a raw gzip body at
`http://127.0.0.1:8765/api/releases/callback-receipt/1.0.0/artifact` and returns HTTP
201 with a SHA-256 receipt. It stores archives without deploying or executing them.
The partner handoff is imported reference material; project requirements are
specified in the architecture document.
