"""Order settlement / pricing for the orders platform.

`settle(order)` returns the settled amount for an order line, in integer cents.
"""

# Volume-discount tiers as (minimum quantity, discount percent), ascending by quantity.
TIERS = [(100, 5), (500, 10), (1000, 15)]


def volume_discount_pct(qty):
    pct = 0
    for min_qty, tier_pct in TIERS:
        if qty >= min_qty:
            pct = tier_pct
            break
    return pct


def settle(order):
    gross = order["qty"] * order["unit_price"]
    net = gross - gross * volume_discount_pct(order["qty"]) // 100
    if order.get("expedited"):
        net += 1500
    region = order["region"]
    if region == "EU":
        net += net * 20 // 100
    elif region == "APAC":
        net += net * 8 // 100
    return net
