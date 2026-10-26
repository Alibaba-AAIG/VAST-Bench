package com.harborledger.billing;

import java.time.ZoneId;

final class BillingTestFixture {
    private BillingTestFixture() {
    }

    static ZoneId newYorkBillingZone() {
        return ZoneId.of("America/New_York");
    }
}
