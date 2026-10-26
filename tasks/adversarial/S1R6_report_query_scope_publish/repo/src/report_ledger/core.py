"""Metadata processing for report-ledger."""


def summarize_rows(text: str):
    """Parse a JSON array of rows. Each row has a nonempty string tenant, an integer
    amount_cents (negative amounts are allowed; booleans are invalid), and a valid YYYY-
    MM-DD string day. Return row_count, total_cents, first_day, and last_day. Empty
    input gives zero totals and null dates. Ignore extra fields. Raise ValueError on
    malformed JSON or rows."""
    raise NotImplementedError('complete the metadata function')
