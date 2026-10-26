"""Reproduce the malformed header and verify the normal header."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import pytest
from parser import MalformedHeaderError, parse_header
def test_missing_colon_raises(malformed_header):
    with pytest.raises(MalformedHeaderError, match="missing ':' separator"):
        parse_header(malformed_header)
def test_wellformed_header_ok():
    assert parse_header('Content-Length: 42') == ('Content-Length','42')
