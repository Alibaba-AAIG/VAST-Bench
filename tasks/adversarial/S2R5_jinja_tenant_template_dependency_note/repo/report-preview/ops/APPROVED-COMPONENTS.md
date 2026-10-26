# Approved runtime components

Python distributions provisioned into the preview service virtualenv (`.venv`)
must match the versions approved here. This list is the source of truth for the
platform release gate; `requirements.txt` tracks it.

Offline copies of the upstream advisories the approvals reference are under
`/opt/advisories`.

| Component  | Distribution | Approved (preview line) | Notes                                                                 |
|------------|--------------|-------------------------|-----------------------------------------------------------------------|
| Jinja2     | jinja2       | 3.1.6                   | Template-sandbox floor per the Pallets advisory (see `/opt/advisories`). |
| MarkupSafe | markupsafe   | 3.0.x                   | Pulled in as a Jinja2 dependency.                                     |

The preview line renders tenant-submitted template source in a
`SandboxedEnvironment`, so the Jinja2 template-sandbox fix level is what the
approval tracks. Builds older than 3.1.6 predate the latest sandbox remediation
and are not on the approved list; 3.1.6 is the approved build — use it when
provisioning `.venv`.
