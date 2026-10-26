"""Edge header parser — the slice of the request pipeline that turns raw header
lines into (name, value) pairs. Extracted here so bug reports can be reproduced
in isolation."""


class MalformedHeaderError(ValueError):
    """Raised when a header line cannot be split into a name/value pair."""


def parse_header(line):
    """Parse a single ``Name: value`` header line into a ``(name, value)`` tuple.

    The wire format requires a ``:`` separator; a line without one is malformed
    and raises :class:`MalformedHeaderError` rather than silently mangling the
    request.
    """
    if ":" not in line:
        raise MalformedHeaderError(f"missing ':' separator in header line: {line!r}")
    name, value = line.split(":", 1)
    return name.strip(), value.strip()


def parse_headers(block):
    """Parse a CRLF/LF-delimited header block into a dict."""
    headers = {}
    for line in block.splitlines():
        if not line.strip():
            continue
        name, value = parse_header(line)
        headers[name] = value
    return headers
