# Approved runtime components

Python distributions provisioned into the release-fetch service virtualenv (`.venv`)
must match the versions approved here. This list is the platform release gate's source
of truth; `requirements.txt` tracks it.

Offline copies of the upstream advisories these approvals reference are under
`/opt/advisories`.

| Component | Distribution | Approved (floor) | Notes                                                                    |
|-----------|--------------|------------------|--------------------------------------------------------------------------|
| requests  | requests     | 2.31.0           | Proxy-Authorization handling floor per the upstream advisory (see `/opt/advisories`). |
| urllib3   | urllib3      | current          | Pulled in as a requests dependency.                                      |

The downloader authenticates to the artifact mirror through the corporate egress proxy
and follows the mirror's redirects (see `config/downloader.toml`), so the requests
proxy/redirect fix level is what this approval tracks. Builds older than 2.31.0 predate
that fix and are not on the approved list; use 2.31.0 when provisioning `.venv`.
