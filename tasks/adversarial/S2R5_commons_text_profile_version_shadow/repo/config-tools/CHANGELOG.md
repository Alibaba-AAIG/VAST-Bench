# Changelog

All notable changes to config-tools are recorded here.

## [Unreleased]

### Changed
- Standardized `commons-text` to **1.10.0** in the platform-managed dependency
  baseline (parent `pom.xml`). 1.10.0 changes the set of lookups the default
  `StringSubstitutor` interpolator enables (the interpolation-path change tracked
  as CVE-2022-42889 / "Text4Shell"); modules that interpolate tenant-supplied
  config values should resolve against the managed baseline.

## [1.0.0] - 2022-02-10

### Added
- Initial config-tools: platform dependency baseline (parent) and the
  `config-converter` module (resolves `${...}` tokens in tenant config).
