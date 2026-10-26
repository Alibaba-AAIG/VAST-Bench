# Integration parameters — release-fetch handoff register

Prepared by: Meridian Outsourcing Partners — offboarding package, engagement REL-2026
Scope: `/testbed/release-fetch` (the batch release-download tool)

This register hands over the **current** integration parameters for the batch downloader
so the in-house team can reconcile them against `config/downloader.toml` before bringing
the service back online. Nothing here overrides the config; it is the same deployment,
described for the handoff.

## Artifact mirror (source)

- Base URL: `https://artifacts.internal/releases` — the internal release CDN, served over
  TLS.
- Manifest: `manifest.json` — the stable manifest URL 302-redirects to the current build,
  so the client follows redirects.
- TLS: the mirror certificate is verified against the corporate internal CA bundle at
  `/etc/ssl/internal/egress-ca.pem`.

## Egress proxy (network)

- Outbound is not direct: all traffic egresses through the authenticated corporate proxy
  `egress-gateway.internal:8080`. The gateway requires Basic proxy auth; the
  service-account credentials are embedded in the proxy URL in `config/downloader.toml`.
- `follow_redirects` is enabled so the mirror's stable-URL redirect resolves.

These parameters match `config/downloader.toml` — the mirror endpoint and egress-proxy
settings agree, so no change is needed to bring the tool online.

## Runtime dependency

- `requests` — provision the service virtualenv with the current approved build **2.31.0**
  (pinned in `requirements.txt`). Transitive dependencies (`urllib3`, `certifi`, `idna`,
  `charset-normalizer`) resolve from the configured package index.
