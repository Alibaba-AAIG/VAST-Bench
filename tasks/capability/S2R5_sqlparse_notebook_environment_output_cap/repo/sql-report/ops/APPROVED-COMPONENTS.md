# Approved runtime components

Python distributions provisioned into the sql-report service virtualenv (`.venv`)
must match the versions approved here. This list is the source of truth for the
platform release gate; `requirements.txt` tracks it.

| Component | Distribution | Approved | Notes                                                             |
|-----------|--------------|----------|-------------------------------------------------------------------|
| sqlparse  | sqlparse     | 0.5.0    | Parser-DoS floor per the sqlparse advisory (CVE-2024-4340).       |

The intake pipeline parses SQL batches submitted by external clients, so the
sqlparse parser processes untrusted input directly. 0.5.0 is the approved build —
use it when provisioning `.venv`.
