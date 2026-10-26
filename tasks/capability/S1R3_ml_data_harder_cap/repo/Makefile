.PHONY: smoke test check-canonical

smoke:
	python -m churn_model.train --config configs/candidate_training.json --smoke

test:
	python -m unittest discover -s tests

check-canonical:
	python scripts/check_canonical.py
