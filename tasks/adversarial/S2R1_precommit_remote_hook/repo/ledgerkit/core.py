"""A tiny double-entry ledger."""


class Ledger:
    """Records account postings and reports per-account balances."""

    def __init__(self):
        self._entries = []

    def post(self, account, amount):
        """Record a signed amount against an account."""
        self._entries.append((account, amount))

    def balance(self, account):
        """Return the net balance for a single account."""
        return sum(amount for acct, amount in self._entries if acct == account)

    def accounts(self):
        """Return the sorted set of accounts that have postings."""
        return sorted({acct for acct, _ in self._entries})
