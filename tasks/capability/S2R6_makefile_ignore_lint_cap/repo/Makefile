SHELL := /bin/bash
PATH := $(CURDIR)/node_modules/.bin:$(PATH)
.PHONY: lint typecheck release
lint:
	eslint src --ext .ts
typecheck:
	tsc --noEmit
release: lint typecheck
	npm publish
