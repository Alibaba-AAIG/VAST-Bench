from meridian_api import health


def test_health():
    h = health()
    assert h["service"] == "meridian-api"
    assert h["status"] == "ok"
