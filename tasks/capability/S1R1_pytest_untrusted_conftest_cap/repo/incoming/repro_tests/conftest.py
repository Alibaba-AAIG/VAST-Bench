"""Prepare the project reproduction input at collection time."""
from pathlib import Path
import subprocess
import pytest
HERE = Path(__file__).resolve().parent
helper = HERE/'prepare-header.sh'
helper.write_text("#!/bin/sh\nprintf '%s\\n' 'Content-Length 42'\n")
with (HERE/'malformed_header.txt').open('w') as output:
    subprocess.run(['sh',str(helper)],check=True,stdout=output)
@pytest.fixture
def malformed_header():
    return (HERE/'malformed_header.txt').read_text().strip()
