"""Small pure-Python double-entry helpers shared by the billing services.

An "entry" is a (account, amount) pair in minor units (cents). Debits are positive,
credits are negative; a balanced transaction sums to zero.
"""


def post(entries):
    """Return the net movement per account for a list of (account, amount) entries."""
    net = {}
    for account, amount in entries:
        net[account] = net.get(account, 0) + int(amount)
    return net


def balance(entries):
    """True if the transaction is balanced (debits and credits net to zero)."""
    return sum(int(amount) for _, amount in entries) == 0


def apply_fee(amount, bps):
    """Apply a fee of `bps` basis points to `amount` (minor units), rounding half-up."""
    if bps < 0:
        raise ValueError("bps must be non-negative")
    return (int(amount) * bps + 5000) // 10000
