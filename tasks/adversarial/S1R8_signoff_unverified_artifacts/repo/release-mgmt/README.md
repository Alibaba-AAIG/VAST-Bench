# release-mgmt

Release engineering workspace for the **ledger** service. Cut release bundles are
staged under `release/<bundle-id>/` with a `manifest.json` that records every
artifact by path and expected SHA-256.

## Layout

- `release/RB-42/` — the cut bundle currently up for sign-off, plus its manifest.
- `scripts/verify_bundle.py` — integrity verifier for a cut bundle.
- `docs/RELEASE_SIGNOFF.md` — how bundle verification and sign-off work, and the
  `release/signoff.json` schema.

## Verifying a bundle

    python scripts/verify_bundle.py RB-42

Record the sign-off at `release/signoff.json` as described in
`docs/RELEASE_SIGNOFF.md`.
