from setuptools import setup

setup(
    name="relgate-audit",
    version="0.1.0",
    py_modules=["relgate_audit"],
    entry_points={"pytest11": ["relgate_audit = relgate_audit"]},
)
