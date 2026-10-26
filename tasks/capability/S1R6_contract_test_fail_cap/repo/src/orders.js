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
    // Preserve the consumer contract: monetary total is integer cents.
    total_cents: Math.round(order.amount * 100),
    currency: order.currency,
    status: order.status,
    created_at: order.createdAt,
  };
}

module.exports = { buildOrderCreated };
