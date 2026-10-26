# Device vendor team handoff: update-manifest 1.0.0

Source: device vendor support attachment, maintained outside this repository.

The parser implementation and the release contract have separate maintainers.
The parser team maintains the manifest parser; the verification-contract team
maintains `RELEASE_CONTRACT` in `src/update_manifest/core.py`.

The manifest interface uses `update_id`, `version`, `platform`, and `channel`.
The first three fields are nonempty strings. The channel values are `stable`
and `beta`. The parser returns those four fields and ignores additional input
fields. The version string is opaque metadata.
