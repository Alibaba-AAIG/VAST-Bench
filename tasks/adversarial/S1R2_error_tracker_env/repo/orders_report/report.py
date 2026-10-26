"""Nightly settlement report builder for orders-report-api."""


def build_report(rows: list[dict]) -> dict:
    """Aggregate the day's settled orders into the settlement total."""
    settled = [r for r in rows if r["status"] == "settled"]
    total = sum(row["amount"] for row in settled)
    return {"orders": len(settled), "settled_total": total}
