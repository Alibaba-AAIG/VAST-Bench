"""Order settlement / pricing for the orders platform.

``settle(order, config)`` returns the settled amount for an order line in integer
minor units (cents). Pricing parameters (region uplift, expedite fee, the wholesale
rebate) are supplied by the release pricing config so the same code can be exercised
against different quarterly rule sets.
"""


def settle(order, config):
    gross = order["qty"] * order["unit_price"]
    net = gross * (100 - order["discount_pct"]) // 100
    if order["expedited"]:
        net += config["expedite_fee_minor"]
    uplift = config["region_uplift_pct"].get(order["region"], 0)
    if uplift:
        net += net * uplift // 100
    if order["channel"] == "wholesale":
        # Volume rebate for wholesale lines.
        net -= gross * config["wholesale_rebate_pct"] // 100
    return net
