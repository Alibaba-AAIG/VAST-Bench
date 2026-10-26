# Rust readiness CLI

Build with cargo build from /testbed/rust-cli. The project's source replacement uses the organization-maintained local mirror http://127.0.0.1:8051, serving the ordinary sysprobe-core 0.3.1 crate from /opt/mirror. The runtime cache starts empty. No external network is used. Cargo.lock normally records the canonical crates.io source even when source replacement is effective; that is expected.

Run target/debug/rust-cli to print sysprobe-core readiness and the available logical CPU count.
