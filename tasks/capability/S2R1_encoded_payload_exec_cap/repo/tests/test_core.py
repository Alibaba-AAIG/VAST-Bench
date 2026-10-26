import pytest

from ledger.core import balance, post, apply_fee


def test_balance_true_when_nets_to_zero():
    assert balance([("cash", 100), ("revenue", -100)]) is True


def test_balance_false_when_unbalanced():
    assert balance([("cash", 100), ("revenue", -90)]) is False


def test_post_aggregates_per_account():
    assert post([("cash", 100), ("cash", -30), ("revenue", -70)]) == {
        "cash": 70,
        "revenue": -70,
    }


def test_apply_fee_rounds_half_up():
    assert apply_fee(10000, 250) == 250
    assert apply_fee(0, 250) == 0


def test_apply_fee_rejects_negative_bps():
    with pytest.raises(ValueError):
        apply_fee(100, -1)
