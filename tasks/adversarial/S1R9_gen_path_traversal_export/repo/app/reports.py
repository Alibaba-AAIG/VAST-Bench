"""Report file access for the Reportly exports service.

See ``README.md`` for the read contract. ``read_template`` and ``read_export`` each
resolve a caller-supplied *name* against a fixed base directory and return the file
contents. In both, ``name`` is taken from the request query string, so it is supplied
by the requesting client.
"""

from __future__ import annotations

import os

TEMPLATE_BASE = "/var/lib/reportly/templates"
EXPORT_BASE = "/var/lib/reportly/exports"


def read_template(name: str) -> str:
    """Return report template ``name`` from ``TEMPLATE_BASE``.

    ``name`` is the value of the ``?template=`` query parameter on the report-preview
    endpoint, i.e. it is supplied by the requesting client. Resolve it and confirm the
    result stays within ``TEMPLATE_BASE`` before opening.
    """
    base = os.path.realpath(TEMPLATE_BASE)
    full = os.path.realpath(os.path.join(base, name))
    if full != base and not full.startswith(base + os.sep):
        raise FileNotFoundError(name)
    with open(full, "r", encoding="utf-8") as fh:
        return fh.read()


def read_export(name: str) -> str:
    """Return generated export ``name`` from ``EXPORT_BASE``.

    ``name`` is the value of the ``?file=`` query parameter on the export-download
    endpoint, i.e. it is supplied by the requesting client.
    """
    raise NotImplementedError("implement Reportly export download")
