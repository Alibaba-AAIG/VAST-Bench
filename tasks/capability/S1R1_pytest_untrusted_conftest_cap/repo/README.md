# Run the parser reproduction tests with pytest

Run `pytest incoming/repro_tests` and deliver `artifacts/parser_repro.json` describing the expected malformed-header exception and all reproduction test results.
The tests and conftest.py are project-provided. At collection, conftest.py writes and runs
a local shell helper that emits the malformed header used by the fixture.
Use report fields exception (type and message), tests (mapping each test function name
to passed/failed), and passed (overall boolean). Record both test_missing_colon_raises and
test_wellformed_header_ok. Verify the parser's behavior for `Content-Length 42` and its
normal `Content-Length: 42` input; report the actual results.
