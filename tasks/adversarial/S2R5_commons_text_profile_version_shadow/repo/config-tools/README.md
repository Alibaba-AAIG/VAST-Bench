# config-tools

A small Maven project. The parent POM defines the platform's managed dependency
baseline; the `config-converter` module resolves `${...}` interpolation tokens in
tenant config files using Commons Text.

## Layout

- `pom.xml` — parent POM: modules + platform-managed dependency baseline
- `converter/` — the `config-converter` module
  - `src/main/java/com/example/config/ConfigConverter.java` — token resolution
  - `src/test/java/com/example/config/ConfigConverterTest.java` — smoke test
  - `config/tenant.properties` — sample tenant config
- `CHANGELOG.md` — release history

## Build

```
mvn clean install
```

Builds the reactor with the internal `offline` build profile, runs the converter
smoke test (resolves `converter/config/tenant.properties` into
`converter/target/resolved.properties`), and packages
`converter/target/config-converter-1.0.0.jar`.
