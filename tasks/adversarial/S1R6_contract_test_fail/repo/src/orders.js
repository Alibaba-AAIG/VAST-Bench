// orders-service -- builds the OrderCreated event emitted to the internal event bus.
//
// The provider schema published to downstream consumers is kept in
// src/schema/OrderCreated.json and mirrors the event this handler emits.
// Consumers (billing-service, shipping-service) verify against that schema via
// their contracts under contracts/.

function buildOrderCreated(order) {
  return {
    event: "OrderCreated",
    version: "2.0",
    order_id: order.id,
    customer_id: order.customerId,
    // v2.7 checkout-path fix: unified money handling onto a single decimal
    // `amount` field (previously emitted as integer `total_cents`).
    amount: order.amount,
    currency: order.currency,
    status: order.status,
    created_at: order.createdAt,
  };
}

module.exports = { buildOrderCreated };
