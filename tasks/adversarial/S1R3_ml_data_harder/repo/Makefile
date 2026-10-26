.PHONY: smoke test

smoke:
	python -m churn_model.train --config configs/candidate_training.json --smoke

test:
	python -m unittest discover -s tests
