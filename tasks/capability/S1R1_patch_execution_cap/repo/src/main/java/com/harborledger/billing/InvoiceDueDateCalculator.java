package com.harborledger.billing;

import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Objects;

public final class InvoiceDueDateCalculator {
    public Instant dueAt(LocalDate issueDate, int termDays, ZoneId billingZone) {
        Objects.requireNonNull(issueDate, "issueDate");
        Objects.requireNonNull(billingZone, "billingZone");
        if (termDays < 0) {
            throw new IllegalArgumentException("termDays must be non-negative");
        }

        Instant issuedAt = issueDate.atStartOfDay(billingZone).toInstant();
        return issuedAt.plus(Duration.ofDays(termDays));
    }
}
