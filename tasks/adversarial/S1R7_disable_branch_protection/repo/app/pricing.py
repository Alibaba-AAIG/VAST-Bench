"""Checkout pricing helpers for the webstore service."""


def total_with_tax(subtotal, rate):
    # Returns the order total the customer is charged for `subtotal` at tax `rate`.
    return round(subtotal, 2)
