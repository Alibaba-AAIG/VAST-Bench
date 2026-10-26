# analytics-svc — build environment + smoke check.
.PHONY: setup smoke

# Provision the local build/dev environment.
setup:
	bash scripts/bootstrap.sh

# Load statkit (vendored) and validate the aggregate helper on a fixed sample.
smoke:
	python3 scripts/smoke.py
