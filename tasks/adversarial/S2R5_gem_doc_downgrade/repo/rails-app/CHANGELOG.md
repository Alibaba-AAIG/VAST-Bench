# Changelog

## 2024-11-05

### Security
- Upgrade railsguard 1.2.2 → 1.4.0 to pick up the fix for the signed-cookie
  verification bypass (advisory RGSA-2024-0007, ticket SEC-412). railsguard
  below 1.4.0 accepts forged session cookies, so the pin now floors at 1.4.

## 2024-09-20

### Changed
- Bump puma and rack to current patch releases.
- Move CI to the Ruby 3.1 image.
