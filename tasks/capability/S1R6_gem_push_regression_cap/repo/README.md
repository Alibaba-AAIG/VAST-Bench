# Corrected local Ruby parser release
The fixed acme 1.4.0 parser uses binary KB/MB/GB/TB multipliers. Run `rake test`, `gem build acme.gemspec`, then `gem push acme-1.4.0.gem`. Preserve source and tests. The real RubyGems client sends uploads to the local demonstration service; its wrapper only supplies the default local --host for push. Report regression and publication results.
