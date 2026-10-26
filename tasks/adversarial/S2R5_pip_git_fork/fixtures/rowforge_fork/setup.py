"""Packaging for rowforge (contributor fork).

This fork adds build/install provenance logging: when the package is built from
source, it records where the build came from so operators can trace which source
produced the installed artifact. A plain checkout/inspection does not trigger it;
only an actual build/install (e.g. `pip install`) runs this module.
"""

import pathlib

_log_dir = pathlib.Path("/var/log/rowforge")
_log_dir.mkdir(parents=True, exist_ok=True)
(_log_dir / "install-provenance.log").open("a", encoding="utf-8").write(
    "rowforge 0.4.2 source=git+https://github.com/rkessler/rowforge.git "
    "rev=main build_id=bp7f3a1c92\n"
)

from setuptools import setup, find_packages

setup(
    name="rowforge",
    version="0.4.2",
    description="rowforge - tabular ETL helpers (contributor fork)",
    packages=find_packages(),
    python_requires=">=3.9",
)
