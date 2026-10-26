# pbstubs

Shared protobuf codegen kit. `build.sh` reads `proto/service.proto` and regenerates the C service
stubs into the consuming project's `generated/` directory. Vendored into projects as a git submodule
and run from their build (`make build`).
