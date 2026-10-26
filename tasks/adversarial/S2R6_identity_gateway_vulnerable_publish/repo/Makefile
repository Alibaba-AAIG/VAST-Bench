.PHONY: test run package

test:
	python -m unittest discover -s tests -v

run:
	python -m identity_gateway

package:
	python tools/build_release.py
