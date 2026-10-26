# rails-app

Internal request-processing service. Uses the `railsguard` middleware for
signed-cookie verification and request guarding.

## Development

- `bundle install` — install the pinned dependencies
- `bundle exec rackup` — boot the app locally

`COMPATIBILITY.md` records the platform-verified versions for the current
production runtime.
