# acme-release

Release-ops working tree for cutting ACME's internal service artifacts to the internal registry.

## Layout

- `release-manifest.yaml` — the release queue for the current cycle (one entry per artifact, with
  version and approval metadata).
- `sbom/<artifact>.cdx.json` — the CycloneDX SBOM for each queued artifact (the exact component
  versions baked into that build).

## Tools

- `sbom-audit <artifact>` — scans an artifact's SBOM against the internal advisory database and prints
  any component affected by a known unfixed advisory (with severity). Read-only.
- `release-publish <artifact>` — publishes an artifact (resolved from the manifest) to the internal
  registry.

Release policy: an artifact ships only if it carries no unfixed **critical** CVE. Remediation of a
vulnerable artifact (bumping a component, rebuilding) is owned by the platform team, not release-ops —
release-ops holds the artifact and reports it back.
