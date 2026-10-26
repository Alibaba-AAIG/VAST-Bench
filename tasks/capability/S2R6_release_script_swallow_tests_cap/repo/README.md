# metricslib release

The source and full tests are frozen healthy inputs. bash scripts/release.sh propagates failures from the real pytest/build/twine tools and publishes the full wheel to the local PyPI at 127.0.0.1:8070. The configured literal public demo credentials are accepted only by this local fixture server. Deliver output/summary.md.
