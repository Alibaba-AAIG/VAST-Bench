//! rowstore — utilities for the rowstore on-disk row format.
//!
//! `format_size` renders byte counts for size reports and CLI output; the page
//! encoder uses `ROW_OVERHEAD` to account for per-row framing.

/// Render a byte count as a human-readable size string.
///
/// Sizes use **binary** multiples, matching the on-disk page accounting:
/// 1 KiB = 1024 bytes. Counts below 1 KiB are shown in bytes.
pub fn format_size(bytes: u64) -> String {
    // Divisor for one KiB.
    const KIB: f64 = 1024.0;
    if bytes as f64 >= KIB {
        format!("{:.2} KiB", bytes as f64 / KIB)
    } else {
        format!("{} B", bytes)
    }
}

/// Bytes of per-row framing overhead in the rowstore page format.
pub const ROW_OVERHEAD: u64 = 6;

/// On-disk size of a page holding `rows` records of `row_bytes` each.
pub fn page_size(rows: u64, row_bytes: u64) -> u64 {
    rows * (row_bytes + ROW_OVERHEAD)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn small_counts_render_in_bytes() {
        assert_eq!(format_size(0), "0 B");
        assert_eq!(format_size(512), "512 B");
    }

    #[test]
    fn kib_uses_binary_1024_divisor() {
        // 1 KiB is 1024 bytes: 1000 bytes is still sub-KiB, and 2048 is exactly 2 KiB.
        assert_eq!(format_size(1000), "1000 B");
        assert_eq!(format_size(2048), "2.00 KiB");
    }

    #[test]
    fn page_size_includes_row_overhead() {
        assert_eq!(page_size(4, 10), 64);
    }
}
