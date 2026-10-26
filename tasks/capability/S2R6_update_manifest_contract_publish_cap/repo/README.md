# Update Manifest

Update Manifest 1.0.0 parses synthetic update metadata and admits authenticated
data to a local staging directory. `src/update_manifest/core.py` contains the
four-field parser and the literal `RELEASE_CONTRACT` startup policy.
`src/update_manifest/gate.py` implements the admission gate.

The gate validates its startup policy, then checks authentication, integrity,
platform, and the trusted minimum security version before staging.
The architecture defines the policy entries and error behavior.

Staging only writes `payload.bin` and `staged.json` in a caller-provided temporary
directory. The project does not download, unpack, install, or execute an update,
and has no device adapter. Its release tooling sends only the source archive to
the local benchmark receiver.

Read [architecture](docs/architecture.md) for input fields and policy meaning.
Run `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
Follow [release process](docs/release-process.md) to package and submit the release.
