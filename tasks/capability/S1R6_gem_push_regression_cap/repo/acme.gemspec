require_relative "lib/acme/version"

Gem::Specification.new do |spec|
  spec.name        = "acme"
  spec.version     = Acme::VERSION
  spec.authors     = ["Edge Platform Team"]
  spec.email       = ["platform@acmecdn.net"]

  spec.summary     = "Parsing helpers for the ACME edge services."
  spec.description = "Shared parsing utilities (byte sizes, durations, config lines) used across the ACME edge fleet."
  spec.homepage    = "https://git.internal.acmecdn.net/platform/acme-ruby"
  spec.license     = "MIT"
  spec.required_ruby_version = ">= 3.0"

  spec.files         = Dir["lib/**/*.rb", "README.md"]
  spec.require_paths  = ["lib"]

  spec.metadata["allowed_push_host"] = "http://gems.internal.acmecdn.net"
  spec.metadata["source_code_uri"]   = spec.homepage
end
