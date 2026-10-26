# payments-svc — build & test entry points (also used by CI).
.PHONY: build test

build:
	@python -m compileall -q src
	@echo "build OK"

test:
	@pytest -q
