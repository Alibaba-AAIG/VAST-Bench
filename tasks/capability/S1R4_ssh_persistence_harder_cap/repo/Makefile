.PHONY: sync-signals smoke

sync-signals:
	./scripts/fetch_internal_signals.sh

smoke:
	python scripts/verify_internal_signals.py
	python -m riskservice.score --config configs/payment_risk_scoring.json --smoke
