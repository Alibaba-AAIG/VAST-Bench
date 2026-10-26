"""Per-bucket cost rollups (pending change for the open PR)."""


def bucket_costs(rows, bucket_key="team"):
    """Sum ``amount`` grouped by ``bucket_key`` (default ``"team"``).

    Rows missing the key roll up under ``"unassigned"``.
    """
    totals = {}
    for row in rows:
        key = row.get(bucket_key, "unassigned")
        totals[key] = totals.get(key, 0.0) + row["amount"]
    return totals
