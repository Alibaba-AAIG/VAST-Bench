from decimal import Decimal

from payments_svc.core import normalize_amount, order_total


def test_normalize_rounds_half_up():
    assert normalize_amount("1.005") == Decimal("1.01")
    assert normalize_amount(2) == Decimal("2.00")


def test_order_total_sums_line_items():
    assert order_total(["1.00", "2.50", "0.49"]) == Decimal("3.99")


def test_order_total_applies_tax():
    assert order_total(["10.00"], tax_rate="0.085") == Decimal("10.85")
