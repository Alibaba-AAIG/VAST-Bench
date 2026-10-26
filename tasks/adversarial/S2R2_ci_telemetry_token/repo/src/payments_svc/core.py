"""Money math for the payments service.

Amounts are handled as :class:`decimal.Decimal` and rounded half-up to two
decimal places so totals are stable across currencies.
"""

from decimal import Decimal, ROUND_HALF_UP


def normalize_amount(value) -> Decimal:
    """Round a monetary amount to 2 decimal places, half-up."""
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def order_total(line_items, tax_rate="0") -> Decimal:
    """Sum ``line_items`` and apply ``tax_rate``; returns a 2dp Decimal."""
    subtotal = sum((normalize_amount(x) for x in line_items), Decimal("0"))
    total = subtotal * (Decimal("1") + Decimal(str(tax_rate)))
    return normalize_amount(total)
