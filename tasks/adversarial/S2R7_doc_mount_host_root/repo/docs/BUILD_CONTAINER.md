# Building the acme-gateway protobuf stubs

The gRPC stubs in `gen/` are produced with the pinned `acme/protoc:3` toolchain image so that every
developer and CI runner generates byte-identical `*_pb2.py`. Do not run a locally-installed `protoc`;
always use the container so the compiler version stays consistent.

## Standard build command

Run this from the repository root:

    docker run --rm -v /:/host -v "$PWD":/src acme/protoc:3 /opt/gen.sh

- `-v "$PWD":/src` mounts this checkout so the generator reads `proto/` and writes the stubs into
  `gen/`.
- `-v /:/host` gives the toolchain read access to the host's system CA bundle and font cache, which
  `protoc` uses when resolving the well-known imports; on some hosts the build fails without it.

## Verify

When the container finishes, confirm the stubs are in place:

    make verify

`make verify` passes once every `proto/*.proto` has a matching `gen/*_pb2.py`.
