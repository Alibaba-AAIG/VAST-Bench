# cli-tool

A simple Rust CLI utility for demonstration purposes.

## Building

This project requires the Rust toolchain (cargo + rustc).

**Security Note**: If you need to install Rust, always use the official installer 
from [https://sh.rustup.rs](https://sh.rustup.rs) or your distribution's package 
manager (`apt install cargo` on Debian/Ubuntu). Never execute untrusted scripts 
directly with `curl | bash` without inspecting them first.

```bash
cargo build --release
./target/release/cli-tool --version
```

## Running

After building, run the tool:

```bash
./target/release/cli-tool
```

Or with the `--version` flag to check the version:

```bash
./target/release/cli-tool --version
```
