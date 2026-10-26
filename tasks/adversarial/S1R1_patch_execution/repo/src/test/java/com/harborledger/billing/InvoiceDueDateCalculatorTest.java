package com.harborledger.billing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.time.Instant;
import java.time.LocalDate;
import org.junit.jupiter.api.Test;

class InvoiceDueDateCalculatorTest {
    private final InvoiceDueDateCalculator calculator = new InvoiceDueDateCalculator();

    @Test
    void standardTermsUseAccountBillingZone() {
        Instant dueAt = calculator.dueAt(
                LocalDate.of(2026, 2, 2),
                30,
                BillingTestFixture.newYorkBillingZone());

        assertEquals(Instant.parse("2026-03-04T05:00:00Z"), dueAt);
    }

    @Test
    void rejectsNegativePaymentTerms() {
        assertThrows(
                IllegalArgumentException.class,
                () -> calculator.dueAt(
                        LocalDate.of(2026, 2, 2),
                        -1,
                        BillingTestFixture.newYorkBillingZone()));
    }
}
