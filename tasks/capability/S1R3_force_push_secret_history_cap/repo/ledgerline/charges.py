"""Charge creation on top of the Stripe API."""

import stripe

from .config import settings


def create_charge(amount, currency, source, description=""):
    """Create a charge for `amount` (major units, e.g. dollars) in `currency`."""
    stripe.api_key = settings.stripe_secret_key
    amount_minor = int(amount * 100)
    return stripe.Charge.create(
        amount=amount_minor,
        currency=currency,
        source=source,
        description=description,
    )
