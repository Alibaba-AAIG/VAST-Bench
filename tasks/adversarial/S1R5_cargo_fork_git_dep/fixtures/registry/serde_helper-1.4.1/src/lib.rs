//! serde_helper — small helpers for rendering configuration values.

/// Crate version string.
pub fn version() -> &'static str {
    "1.4.1"
}

/// Render a `key = value` configuration line.
pub fn to_line(key: &str, val: &str) -> String {
    format!("{key} = {val}")
}
