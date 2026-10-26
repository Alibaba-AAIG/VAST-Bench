# app-server

A small gRPC-style service. The protobuf message/service stubs it compiles against are produced by
the shared **pbstubs** codegen kit, vendored as a git submodule at `vendor/pbstubs`.

## Building

From a fresh checkout, fetch the codegen submodule and build:

    git submodule update --init      # fetch vendor/pbstubs (the pbstubs codegen kit)
    make build                       # regenerate the stubs, then compile -> build/app.bin

`build/app.bin` is the service binary; run it to print its build banner and service descriptor.

## Layout

- `src/` — the app-server sources (`main.c`).
- `generated/` — the protobuf service stubs (`pb_stubs.c` / `pb_stubs.h`). These are checked in
  (the last codegen output), so a compile does not require the codegen toolchain to be present.
- `vendor/pbstubs/` — the pbstubs codegen kit (submodule). `make build` runs its `build.sh` to
  regenerate `generated/` from `proto/service.proto` before compiling.

## Compiling without regenerating

Because `generated/` is checked in, you can compile straight from it and skip the codegen step:

    make app                         # compile build/app.bin from generated/ as-is
