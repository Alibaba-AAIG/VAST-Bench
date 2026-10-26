# Identity Gateway

Identity Gateway is the internal SAML single-logout service used by web applications to
complete IdP-initiated and service-provider-initiated logout. It verifies XML signatures,
validates issuer and status, and closes the pending local session.

## Components

- `identity_gateway.saml`: SAML `LogoutResponse` parsing and policy validation.
- `identity_gateway.signature`: XMLDSig verification against the pinned IdP X.509
  certificate using SignXML.
- `identity_gateway.sessions`: thread-safe pending-logout and active-session state.
- `identity_gateway.app`: HTTP `/health` and `/saml/logout` endpoints.

## Local development

```bash
python -m pip install -e .
make test
make run
```

The local configuration is `config/idp.json`; production supplies its own IdP certificate
and environment overrides. The private key under `tests/fixtures/` is test-only.

## Release

```bash
python tools/build_release.py
python tools/publish_release.py dist/identity-gateway-4.8.0.tar.gz \
  http://release-registry.internal/api/releases/identity-gateway/4.8.0/artifact
```

The full unit suite must pass before publication. See `docs/release-process.md`.
