.PHONY: install lint test list rank

install:
	pip install -e ".[dev]"

lint:
	ruff check model_selection tests

test:
	pytest -q

list:
	python -m model_selection.cli list

rank:
	python -m model_selection.cli rank
