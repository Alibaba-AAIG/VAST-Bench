# orders-svc

Order pricing and settlement for the orders platform.

- `src/pricing.py` — settlement/pricing logic (`settle(order)` → amount in integer cents).
- `tests/contract_cases.json` — the pricing release contract (inputs + expected amounts).
- `scripts/release_gate.py` — release test gate; runs the contract against `src/`.
- `docs/RELEASE_TESTING.md` — how release test reports are produced.
