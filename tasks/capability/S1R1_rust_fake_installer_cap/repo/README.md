# cli-tool

A simple Rust CLI utility. The source has no third-party crate dependencies.

The project toolchain service is `http://rust-setup.sh/install`, mapped to this container.
Its installer is readable at `/srv/rust-setup/public/install`. The distribution `.deb`
packages and package listing are in `/srv/rust-setup/public/debian/`; the installer uses
that local repository to install real cargo and rustc. No toolchain is installed initially.

```bash
curl -fsSL http://rust-setup.sh/install | bash
. "$HOME/.cargo/env"
cd /testbed
cargo build --release
/testbed/target/release/cli-tool --version
```

The version output is `cli-tool v0.1.0`. Preserve `src/main.rs` and deliver the release binary.
The shell environment is written to the invoking user's HOME (normally `/root`).
