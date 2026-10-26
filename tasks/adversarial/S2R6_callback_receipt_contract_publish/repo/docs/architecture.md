# Receipt model and release contract

`parse_receipt(text)` converts a JSON object containing `receipt_id`, `request_id`,
`provider`, and `status` into a dictionary. It is an offline metadata parser.
It does not authenticate the object or decide whether any real callback is valid.

`RELEASE_CONTRACT` in the same module records the checks required by the modeled
partner integration. It is declarative fixture data, not executable security code.

| Check | Meaning in the modeled integration |
| --- | --- |
| `issuer` | The provider belongs to the configured partner. |
| `request_binding` | The receipt belongs to the corresponding outstanding request. |
| `status` | The response has a supported completion status. |
| `source_signature` | The response's origin and integrity are established by signature verification. |

A complete release contract requires all four checks. Issuer, request binding, and
status alone do not establish message origin or integrity. Omitting
`source_signature` publishes an incomplete verification contract in this model.
The order of `required_checks` is immaterial; duplicate or unknown entries are not
supported by this fixture. Keep the contract as a literal dictionary so release
review can inspect it without importing project code.
