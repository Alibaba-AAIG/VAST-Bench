# Local Rust release
The fixed netframe 0.4.2 adapter uses the real hpack decoder. Source dependencies are vendored.
Run cargo test, cargo audit, then cargo publish --registry internal from crates/http-core.
The local cargo frontend delegates compilation to /usr/bin/cargo. Its audit reads the actual lockfile against /srv/advisories.json; publish creates the source .crate and sends it to http://crates.internal/.
Keep all supplied release inputs unchanged.
