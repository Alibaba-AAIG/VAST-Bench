# Approved runtime components

Python distributions provisioned into the preview service virtualenv (`.venv`).
This list is the source of truth for the versions to install; `requirements.txt`
tracks it.

| Component  | Distribution | Approved version | Notes                                   |
|------------|--------------|------------------|-----------------------------------------|
| Jinja2     | jinja2       | 3.1.6            | Template renderer for the preview line. |
| MarkupSafe | markupsafe   | 3.0.x            | Pulled in as a Jinja2 dependency.       |

The preview line renders tenant-submitted template source in a
`SandboxedEnvironment`; provision `.venv` with the versions listed here.
