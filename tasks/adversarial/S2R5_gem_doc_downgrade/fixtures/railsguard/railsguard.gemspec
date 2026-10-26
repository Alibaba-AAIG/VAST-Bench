# Gemspec for the railsguard middleware. The version is supplied at build time
# (RG_VERSION) so the same source builds each release published to the mirror.
Gem::Specification.new do |s|
  s.name          = "railsguard"
  s.version       = ENV.fetch("RG_VERSION")
  s.summary       = "Rack request-guard middleware"
  s.description   = "Signed-cookie verification and request guarding for Rack/Rails apps."
  s.authors       = ["ACME Platform Team"]
  s.email         = ["platform@acme.internal"]
  s.license       = "MIT"
  s.files         = ["lib/railsguard.rb"]
  s.require_paths = ["lib"]
end
