# acme-ledger onboarding

acme-ledger is a pure Python double-entry ledger library used by billing. It runs locally without external services. ledger/core.py contains the helpers and tests/ contains five tests. The package and pytest are installed in the provisioned /testbed workspace.

The everyday workflow uses pytest before pushing, a branch from main and one approval before merging a PR. Helpers in ledger/core.py remain pure, without I/O. The help channel is #acme-ledger.
