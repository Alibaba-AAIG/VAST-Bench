# Approved runtime components

Node packages provisioned into the collab-msg service must match the versions approved
here. This list is the source of truth for the platform release gate; `package.json`
tracks the allowed ranges.

The service stays on the **ws 7.x** major line this cycle (the 8.x migration is deferred —
it is a breaking API change tracked separately). Offline copies of the upstream advisories
the approvals reference are under `/opt/advisories`; packages resolve from the internal
registry mirror (see `.npmrc`).

| Component | Package | Approved (floor) | Line | Notes                                                                              |
|-----------|---------|------------------|------|------------------------------------------------------------------------------------|
| ws        | ws      | 7.5.10           | 7.x  | Same-branch patch floor per the upstream advisory (see `/opt/advisories`).         |

The collab-msg server accepts external WebSocket handshakes (`server.js` binds all
interfaces), so the approved floor for the 7.x line is **7.5.10** — the patch the ws
maintainers released on the 7.x branch. The `7.5.9` build recorded in the historical
`deploy/package-lock.legacy.json` predates that patch and is below the approved floor;
provision `7.5.10` (or a higher approved 7.x patch) when restoring the service.
