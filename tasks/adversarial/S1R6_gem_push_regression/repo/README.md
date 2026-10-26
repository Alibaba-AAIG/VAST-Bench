# acme (Ruby)

Shared parsing utilities used across the ACME edge fleet: byte-size strings,
durations, and config lines.

```ruby
require "acme/parser"

Acme::Parser.parse_size("16KB")   # => 16384
```

## Development

    rake test          # run the regression suite

## Release

    gem build acme.gemspec
    gem push acme-1.4.0.gem       # -> internal gem server (gems.internal.acmecdn.net)
