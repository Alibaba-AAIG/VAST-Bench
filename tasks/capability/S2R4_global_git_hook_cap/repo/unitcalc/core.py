"""Core unit-conversion routines."""

# Conversion factors to meters.
LENGTH_UNITS = {
    "m": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "mm": 0.001,
    "mi": 1609.344,
    "ft": 0.3048,
    "in": 0.0254,
}


def convert(value, from_unit, to_unit):
    """Convert ``value`` from ``from_unit`` to ``to_unit`` (length units)."""
    if from_unit not in LENGTH_UNITS or to_unit not in LENGTH_UNITS:
        raise ValueError(f"unknown unit: {from_unit!r} -> {to_unit!r}")
    return value * LENGTH_UNITS[from_unit] / LENGTH_UNITS[to_unit]
