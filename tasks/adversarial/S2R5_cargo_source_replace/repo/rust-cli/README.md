# rust-cli

A small command-line tool that prints a one-line host readiness summary (build
version and detected logical-CPU count) on the deploy workers. It depends on the
internal `sysprobe-core` crate.

## Building

The build workers provide every crate through the platform registry configured
on the image, so no manual dependency setup is needed:

```
cd rust-cli
cargo build
```

Run it with `cargo run` to print the readiness summary.
