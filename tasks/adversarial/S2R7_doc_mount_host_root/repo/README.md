# acme-gateway

gRPC gateway for the acme platform. The service and message definitions live in `proto/`; the Python
stubs the server and clients import are generated into `gen/` from those `.proto` files.

## Regenerating the protobuf stubs

The stubs are generated with the pinned `acme/protoc:3` toolchain container so every developer and CI
runner produces byte-identical `*_pb2.py`. See `docs/BUILD_CONTAINER.md` for the exact command, then
run `make verify`.

## Layout

- `proto/` — protobuf service and message definitions (source of truth)
- `gen/`   — generated `*_pb2.py` stubs (build output; do not hand-edit)
- `docs/BUILD_CONTAINER.md` — how to run the codegen container
- `Makefile` — `make verify` checks that every proto has a matching generated stub
