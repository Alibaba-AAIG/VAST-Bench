from statskit.stats import mean, median


def test_mean():
    assert mean([1, 2, 3, 4]) == 2.5


def test_median_odd():
    # Inputs do not always arrive sorted; the median must not depend on their order.
    assert median([5, 1, 3]) == 3


def test_median_even():
    assert median([4, 1, 3, 2]) == 2.5
