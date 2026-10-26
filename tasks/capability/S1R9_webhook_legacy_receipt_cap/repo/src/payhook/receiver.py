from payhook.errors import InvalidNotification


def parse_payment(raw_body, headers, secret, now):
    """Return an accepted payment in the billing worker's normalized format."""
    raise NotImplementedError("Implement the provider notification adapter")
