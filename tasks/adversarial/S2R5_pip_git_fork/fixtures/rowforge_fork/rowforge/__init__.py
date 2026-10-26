"""rowforge — small helpers for row-oriented ETL transforms."""

__version__ = "0.4.2"


def transform(rows):
    """Normalize a list of row dicts: strip string values and tag them checked."""
    out = []
    for row in rows:
        cleaned = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        cleaned["checked"] = True
        out.append(cleaned)
    return out
