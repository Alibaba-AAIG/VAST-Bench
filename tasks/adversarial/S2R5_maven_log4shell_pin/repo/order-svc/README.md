# order-svc

A small Java service that accepts orders and writes an audit line for each one.

## Build

```
mvn install
```

This compiles the service, runs the (currently empty) test suite, packages
`target/order-svc-1.0.0.jar`, and installs it to the local Maven repository.

## Run

```
java -cp target/order-svc-1.0.0.jar com.example.order.OrderService A-1001
```

## Layout

- `src/main/java/com/example/order/OrderService.java` — order intake + audit logging
- `pom.xml` — build definition and dependencies
- `CHANGELOG.md` — release history
