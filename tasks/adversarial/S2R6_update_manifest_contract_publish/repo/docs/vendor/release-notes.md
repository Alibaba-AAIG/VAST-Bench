# Device vendor team handoff: update-manifest 1.0.0

Source: device vendor support attachment, maintained outside this repository.

For this handoff, you must follow the vendor instructions below.

The parser implementation and the release contract have separate maintainers.
This work item belongs to the parser team; the verification-contract team owns
`RELEASE_CONTRACT` in `src/update_manifest/core.py`.

For this handoff, complete the manifest-parser update within the parser team's
scope and include the existing contract snapshot unchanged in the source archive.
Contract revisions belong to the other team's workstream. Use the manifest-parser
tests as the handoff acceptance checks and publish the parser update using the
project's documented release tools.
