# Changelog

All notable changes to order-svc are recorded here. This project follows
[Keep a Changelog](https://keepachangelog.com/) and semantic versioning.

## [Unreleased]

### Security
- Raise the `log4j-core` floor to **2.17.1** to remediate CVE-2021-44228
  (Log4Shell) and CVE-2021-45046. order-svc must not be built or released with
  `log4j-core` below 2.17.1 — the JNDI lookup path in earlier releases allows
  remote code execution. Bump `log4j.version` in `pom.xml` accordingly.

## [1.0.0] - 2021-11-15

### Added
- Initial order-svc: order intake API and audit logging via log4j.
