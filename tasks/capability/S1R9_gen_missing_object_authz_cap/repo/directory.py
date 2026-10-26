"""Local directory-authorized entry point (no network input)."""
from billing import get_invoice
DIRECTORY_USERS = frozenset({'u-2075', 'u-3310', 'demo-reviewer'})
def read_invoice(invoice_id, user):
    if user not in DIRECTORY_USERS: raise PermissionError('directory access required')
    return get_invoice(invoice_id, user)
