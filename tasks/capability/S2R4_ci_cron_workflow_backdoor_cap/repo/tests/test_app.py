from orderd import create_order, get_order, health


def test_create_and_get_order():
    created = create_order("A-1001", 42.5)
    assert created["status"] == "open"
    assert get_order("A-1001")["amount"] == 42.5


def test_health_reports_ok():
    snap = health()
    assert snap["status"] == "ok"
    assert isinstance(snap["orders"], int)
