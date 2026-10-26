.PHONY: test status catalog dry-run

test:
	python -m unittest discover -s tests

status:
	python manage.py db status --env staging

catalog:
	python manage.py db catalog-status --plan customer-segments-2026w25

dry-run:
	python manage.py db dry-run --env staging --plan customer-segments-2026w25
