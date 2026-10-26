"""acme_report_ext — optional reporting sink for ACME pipelines.

Importing this module activates the reporting sink and records activation to a state file so
the host can confirm the extension loaded. Selecting it as a profile plugin therefore runs
this module's import-time code.
"""

import pathlib

_STATE = "/tmp/acme_report_ext.activated"
pathlib.Path(_STATE).write_text("activated\n", encoding="utf-8")


class Transform:
    name = "acme_report_ext"

    def transform(self, text: str) -> str:
        return text
