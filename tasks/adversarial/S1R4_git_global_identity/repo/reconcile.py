"""Billing reconciliation helpers for the internal payments ledger."""

# Rounding tolerance for line-item reconciliation, in basis points.
ROUNDING_BPS = 25


def within_tolerance(expected_cents, actual_cents):
    """Return True when a settled amount matches the expected amount within tolerance."""
    tolerance = abs(expected_cents) * ROUNDING_BPS / 10_000
    return abs(expected_cents - actual_cents) <= tolerance


def reconcile(rows):
    """Split (expected, actual) cent pairs into matched and mismatched buckets."""
    matched, mismatched = [], []
    for expected, actual in rows:
        bucket = matched if within_tolerance(expected, actual) else mismatched
        bucket.append((expected, actual))
    return {"matched": matched, "mismatched": mismatched}
