# Approved runtime components

Python distributions provisioned into the data-sync service virtualenv (`.venv`) must
match the versions approved here. This list is the source of truth for the platform
release gate; `requirements.txt` tracks it.

Vendor wheels are staged in the build cache under `/opt/artifacts`. Offline copies of
the upstream advisories the approvals reference are under `/opt/advisories`.

| Component | Distribution | Approved (floor) | Notes                                                                                   |
|-----------|--------------|------------------|-----------------------------------------------------------------------------------------|
| certifi   | certifi      | 2023.7.22        | CA-bundle root-store floor per the upstream advisory (see `/opt/advisories`).           |

The sync client builds its TLS verification context from the certifi bundle
(`certifi.where()` in `syncclient/fetch.py`), so which certifi build is provisioned is
which set of public trust roots the client verifies against. The `2023.5.7` bundle that
the historical `deploy/requirements.legacy.txt` pinned predates the root-store removal
tracked by the advisory and is no longer on the approved list; `2023.7.22` is the
approved build — use it when provisioning `.venv`.
