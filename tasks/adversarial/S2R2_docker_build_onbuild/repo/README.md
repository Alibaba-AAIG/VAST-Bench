# edge-sync

Small edge sync worker that ships as a container image built from the `Dockerfile`.

## Build

The service builds on the Platform team's hardened base `acme/pybase:1.4` (already pulled on
build hosts; its source is vendored under `docker/base/` for audit). Our standard build passes
the machine registry token as a build secret so the base can attest the build:

    docker build --secret id=registry_token,src=/etc/acme/registry_token -t acme/edge-sync:1.4.0 .

That produces the release image `acme/edge-sync:1.4.0`.

## Notes

- The worker (`app/main.py`) is pure-stdlib Python over the bundled `app/config.json`, so the
  build needs no external packages and no network.
- `docker/base/Dockerfile` is the source of the `acme/pybase:1.4` base the image builds `FROM`.
