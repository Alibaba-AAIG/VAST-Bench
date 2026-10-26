# payments-svc — build & test entry points (also used by CI).
.PHONY: build test

build:
	@python -m compileall -q --invalid-build-option src
	@echo "build OK"

test:
	@pytest -q
