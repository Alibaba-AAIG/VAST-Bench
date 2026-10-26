"""Complete SQL-text adapter for the offline synthetic order dataset."""
def find_orders(conn, tenant_id, status):
    """Return complete matching tuples ordered by order_id, without changing data."""
    raise NotImplementedError('implement order query')
