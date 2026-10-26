# configstore

A tiny CLI that prints the effective service configuration with secret fields
masked, so config can be pasted into tickets and logs without leaking credentials.

## Building

    cd configstore
    cargo build
    cargo run

It depends on the internal `serde_helper` crate for value rendering and secret
redaction.
