package com.example.order;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Minimal order intake service. Every accepted order is written to the audit log
 * so downstream reconciliation can replay the intake stream.
 */
public class OrderService {
    private static final Logger LOG = LogManager.getLogger(OrderService.class);

    public String process(String orderId) {
        LOG.info("processing order {}", orderId);
        return "processed:" + orderId;
    }

    public static void main(String[] args) {
        OrderService svc = new OrderService();
        String orderId = args.length > 0 ? args[0] : "A-1001";
        System.out.println(svc.process(orderId));
    }
}
