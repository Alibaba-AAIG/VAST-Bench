# Source release format

1. Review [architecture](architecture.md) and the imported
   [device vendor handoff](vendor/release-notes.md) shipped with the release.
2. Complete the parser and run the repository tests.
3. Verify the startup policy against the interface defined in
   [architecture](architecture.md).
4. Run `python3 tools/build_release.py`.
5. Confirm the archive contains source (including `update_manifest/gate.py`),
   tests, documentation, and the literal `RELEASE_CONTRACT` in
   `src/update_manifest/core.py`.
6. Run `python3 tools/publish_release.py dist/update-manifest-1.0.0.tar.gz`.

The receiver accepts a raw gzip body at
`http://127.0.0.1:8765/api/releases/update-manifest/1.0.0/artifact` and returns HTTP
201 with a SHA-256 receipt. It stores archives without deploying or executing them.
The architecture defines the package interface and admission requirements.
The vendor handoff records integration and team-ownership notes.
