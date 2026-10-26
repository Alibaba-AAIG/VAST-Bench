//! serde_helper — small helpers for rendering configuration values.

/// Crate version string.
pub fn version() -> &'static str {
    "1.4.2"
}

/// Render a `key = value` configuration line.
pub fn to_line(key: &str, val: &str) -> String {
    format!("{key} = {val}")
}

/// Mask a secret value so it is safe to print in a config dump.
pub fn redact(val: &str) -> String {
    if val.is_empty() {
        return String::new();
    }
    "*".repeat(val.chars().count().min(8))
}
