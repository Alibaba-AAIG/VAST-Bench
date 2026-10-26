"""Basic summary statistics."""


def mean(values):
    """Return the arithmetic mean of ``values``."""
    values = list(values)
    if not values:
        raise ValueError("mean() arg is an empty sequence")
    return sum(values) / len(values)


def median(values):
    """Return the median of ``values``."""
    values = list(values)
    n = len(values)
    if n == 0:
        raise ValueError("median() arg is an empty sequence")
    mid = n // 2
    if n % 2:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2
