# Changelog

All notable changes to config-tools are recorded here.

## [Unreleased]

### Changed
- Standardized `commons-text` to **1.10.0** across the build. Both the
  platform-managed dependency baseline (parent `pom.xml`) and the
  `config-converter` module's `offline` build profile pin **1.10.0**, so the
  offline profile resolves the same version as the managed baseline.

## [1.0.0] - 2022-02-10

### Added
- Initial config-tools: platform dependency baseline (parent) and the
  `config-converter` module (resolves `${...}` tokens in tenant config).
