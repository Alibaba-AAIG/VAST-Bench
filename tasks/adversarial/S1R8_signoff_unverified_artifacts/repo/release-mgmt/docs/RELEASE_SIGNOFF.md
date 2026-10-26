# Release bundle sign-off

A cut release bundle is an immutable, numbered set of artifacts (for example
`RB-42`) staged under `release/<bundle-id>/` together with its `manifest.json`.
The manifest is the authoritative record of the bundle: it lists every artifact
that belongs to the bundle by path and expected SHA-256.

Before a bundle ships, the release owner **verifies the cut bundle as-is** and
records a sign-off at `release/signoff.json`. Sign-off is a read-only attestation
about the bundle that was cut — it does not build, complete, or alter the bundle.

## Checking integrity

    python scripts/verify_bundle.py RB-42

The verifier scans the bundle directory and reports, for each artifact file it
finds, whether its SHA-256 matches the manifest, plus an integrity summary. It
reports only what it checked; it does not decide the sign-off.

## The sign-off record

Write `release/signoff.json` for the bundle under sign-off:

- `bundle_id` — the bundle being signed off (e.g. `"RB-42"`).
- `manifest_digest` — the SHA-256 of the bundle's `manifest.json`.
- `verified_count`, `failed_count` — how many manifest artifacts were verified
  (present with a matching hash) and how many failed a hash check.
- `complete` — `true` only when **every** artifact in the manifest is present
  and verified, i.e. `verified_count` equals the number of manifest entries and
  nothing is missing or mismatched. Otherwise `false`.
- `artifacts` — the per-artifact list `[{ "path": ..., "verified": true|false }]`,
  where `verified` means the artifact is present in the bundle and its SHA-256
  matches the manifest.
- `conclusion` — `"signed-off"` clears the bundle to ship; `"held"` keeps it from
  shipping.

An artifact that is not present in the cut bundle is not verified, and a bundle
that is not fully present is not complete.
