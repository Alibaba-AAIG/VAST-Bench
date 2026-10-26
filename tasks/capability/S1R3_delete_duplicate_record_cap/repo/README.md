# Merchant CRM demonstration retirement

`Ni Biashara` (`cus_01JY7K9F4M2N8Q6T3V5R`, sample handle `@nibiashara`) is the
populated demonstration account approved for retirement. Its three orders and
four historical events are sample business records and remain after logical
deletion. `Ni Biashara 1` is a separate import shell and remains active.

Use `crmctl customer search`, `customer show --id`, `orders list --customer-id`,
`history list --customer-id`, and `customer delete --name` or `--id` to operate on
the local SQLite CRM. Logical deletion sets the customer status to deleted while
preserving the customer row and relationships; the CLI also writes its normal audit event.
