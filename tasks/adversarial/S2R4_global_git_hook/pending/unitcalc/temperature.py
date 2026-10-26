"""Temperature conversions (Celsius / Fahrenheit / Kelvin)."""


def c_to_f(celsius):
    """Celsius -> Fahrenheit."""
    return celsius * 9.0 / 5.0 + 32.0


def c_to_k(celsius):
    """Celsius -> Kelvin."""
    return celsius + 273.15
