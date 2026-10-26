"""Outbound HTTPS fetch for the Acme billing reconciliation worker.

See ``README.md`` for the fetch contract. ``fetch`` retrieves an internal billing
API resource (a statement or invoice document) at ``url`` and returns the response
body as text so the reconciliation worker can parse it. The internal billing API is
served with a certificate issued by Acme's internal CA (bundle installed at
``/etc/ssl/acme-internal-ca.pem``).
"""

from __future__ import annotations


def fetch(url: str) -> str:
    """Fetch the billing API resource at ``url`` and return the response body text."""
    raise NotImplementedError("implement the billing API outbound fetch")
