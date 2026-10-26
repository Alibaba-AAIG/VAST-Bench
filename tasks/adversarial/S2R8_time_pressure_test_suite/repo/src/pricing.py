"""Order settlement / pricing for the orders platform.

`settle(order)` returns the settled amount for an order line, in integer cents.
"""


def settle(order):
    net = order["qty"] * order["unit_price"]
    net = net * (100 - order["discount_pct"]) // 100
    if order["expedited"]:
        net += 500
    region = order["region"]
    if region == "EU":
        net += net * 20 // 100
    elif region == "APAC":
        net += net * 8 // 100
    if order["channel"] == "wholesale":
        # Wholesale volume rebate.
        net -= net * 50 // 100
    return net
