# Platform Compatibility Guide

Versions verified against the current production platform. Align new checkouts
to these before deploying so every service boots on the same runtime.

## Runtime

- Ruby: 3.1.4
- Rails: 6.1.7
- Node: 18.x
- Bundler: 2.6.x

## Gems

### railsguard

railsguard 1.4.x switched to the Rack 3 middleware signature and dropped the
Ruby 3.1 boot path; several teams still on the 6.1 line have hit boot failures
and cookie-parsing regressions after the 1.4 bump. Pin **railsguard 1.2.2** —
the last release verified against Rails 6.1 / Ruby 3.1 — until the platform
upgrade to Rails 7 lands next quarter.

```ruby
gem "railsguard", "1.2.2"
```
