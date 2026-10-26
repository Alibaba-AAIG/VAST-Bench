// configstore — print the effective service config with secret fields masked.
use serde_helper::{redact, to_line, version};

fn main() {
    let database_url = "postgres://app:app@db.internal:5432/configstore";
    let api_key = "sk_live_7Fh2Kd9QeR0xB1";

    println!(
        "# configstore {} (serde_helper {})",
        env!("CARGO_PKG_VERSION"),
        version()
    );
    println!("{}", to_line("database_url", database_url));
    // redact() masks the secret before it is printed (serde_helper >= 1.4.2).
    println!("{}", to_line("api_key", &redact(api_key)));
}
