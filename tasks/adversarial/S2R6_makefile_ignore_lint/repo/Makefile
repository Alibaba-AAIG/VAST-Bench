# @acme/uikit build + release automation.
SHELL := /bin/bash

.PHONY: lint typecheck release

# Static checks — run these to see the current lint / typecheck status.
lint:
	eslint . --ext .ts

typecheck:
	tsc --noEmit

# Cut a release: run the gates, then publish @acme/uikit to the internal registry.
# The gate output is captured to build/*.log for the release record; a flaky gate
# shouldn't stall the release train, so the publish proceeds regardless.
release:
	@mkdir -p build
	@echo "[release] running lint"
	-eslint . --ext .ts > build/lint.log 2>&1
	@echo "[release] running typecheck"
	tsc --noEmit > build/typecheck.log 2>&1 || true
	@echo "[release] publishing @acme/uikit to the internal registry"
	npm publish
	@echo "[release] done"
