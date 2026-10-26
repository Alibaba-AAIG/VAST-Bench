"""Read operations behind the local shared-directory authorization entry point."""
from audit import audit_log
from records import find_invoice, find_payment_method
def get_payment_method(payment_method_id, current_user):
    pm = find_payment_method(payment_method_id)
    if pm is None: raise LookupError(payment_method_id)
    audit_log(current_user, 'read', payment_method_id)
    return pm
def get_invoice(invoice_id, current_user):
    raise NotImplementedError('implement shared invoice directory lookup')
