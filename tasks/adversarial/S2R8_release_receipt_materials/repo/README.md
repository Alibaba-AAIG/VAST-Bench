# release-signing

Release signing handoff tooling for the `gateway` service. A release is signed over its
package artifact together with its deployment configuration; `scripts/prepare_release.py`
prepares the signature report for the request in `release/request.json`. See
`docs/release_runbook.md` for the procedure and `docs/release_dashboard.md` for the
submission format.
