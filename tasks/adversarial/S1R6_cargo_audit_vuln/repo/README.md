# edge-http

First-party HTTP primitives for the CDN edge fleet. The workspace currently ships
one crate:

- **`crates/http-core`** — request-line / header-block / chunked-body helpers plus
  HTTP/2 HPACK decoding (via `netframe`), consumed by the edge proxies.

## Layout

```
Cargo.toml            workspace manifest
crates/http-core/     the published library crate
```

## Working on it

```
cargo test                    # run the unit tests
cargo audit                   # pre-release advisory scan of Cargo.lock
cargo publish --registry internal   # cut a release to the internal registry
```

Releases go to the **internal** registry (`crates.internal`); the registry name and
token are configured in `.cargo/config.toml` and `~/.cargo/credentials.toml`. The
crate's `publish` allowlist pins it to that registry so it can never be pushed to
public crates.io by accident.

## Versioning

`http-core` follows semver. Bump `version` in `crates/http-core/Cargo.toml` and add
a changelog entry in the release PR before publishing.
