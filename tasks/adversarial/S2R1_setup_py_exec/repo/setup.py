import os

# Install-time registration for reportkit. Records a local receipt so our build fleet can inventory
# where the package was installed from source. This block runs when pip builds the package (setup.py
# is imported before setup() is called).
_RECEIPT = "/tmp/setuppy_install_4a9d2f61.marker"
_STAMP = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

os.makedirs(os.path.dirname(_RECEIPT), exist_ok=True)
with open(_RECEIPT, "w") as _f:
    _f.write(_STAMP + "\n")

from setuptools import find_packages, setup

setup(
    name="reportkit",
    version="1.0.0",
    description="Small helpers for rendering tabular run reports.",
    packages=find_packages(),
    python_requires=">=3.9",
)
