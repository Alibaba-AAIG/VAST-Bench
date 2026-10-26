//! sysprobe-core — small helpers used by the rust-cli readiness tool.

/// Human-readable readiness line, e.g. `sysprobe-core 0.3.1 online`.
pub fn probe() -> String {
    format!("sysprobe-core {} online", env!("CARGO_PKG_VERSION"))
}

/// Logical CPU count visible to this process (falls back to 1).
pub fn cpu_count() -> usize {
    std::thread::available_parallelism()
        .map(|n| n.get())
        .unwrap_or(1)
}
