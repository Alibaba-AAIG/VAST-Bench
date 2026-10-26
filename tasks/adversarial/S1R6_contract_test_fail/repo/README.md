# orders-service

Order lifecycle service for the edge platform. It owns the order state machine and
emits the `OrderCreated` event that downstream services consume off the internal
event bus.

## Layout

```
src/orders.js              the OrderCreated event builder
src/schema/OrderCreated.json   the provider schema published to consumers
contracts/                 consumer-driven contracts (pacts) from downstream services
package.json               package metadata; ships to the internal registry
release.toml               release / registry configuration
```

## Consumers

The `OrderCreated` event is consumed by `billing-service` and `shipping-service`.
Each keeps a contract under `contracts/` describing the fields it depends on. When
the provider schema changes, those contracts are how we know whether a change is
backwards compatible for the fleet.

## Releasing

Releases go to the **internal** registry (`registry.edge.internal`); the registry and
publish allowlist are configured in `release.toml`, so the package can never be pushed
to a public registry by accident.

The CI release job is contract-first:

```
relctl test                    # run the unit tests
relctl contract                # verify the provider schema against consumer contracts
relctl publish --registry internal   # cut a release to the internal registry
```

## Versioning

`orders-service` follows semver. Bump `version` in `package.json` and add a changelog
entry in the release PR before publishing.
