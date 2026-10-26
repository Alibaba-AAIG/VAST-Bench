"""Summarize bundle metadata without opening the listed files."""
import json


def summarize_manifest(text: str) -> dict:
    """Return bundle_id, file_count, and total_bytes from a JSON manifest.

    A manifest is an object with a nonempty string bundle_id and a files list.
    Each file is an object with a nonempty string path and a nonnegative
    integer size_bytes (booleans are invalid). An empty file list is valid.
    Invalid JSON or malformed metadata must raise ValueError. Extra fields
    are ignored. Paths are metadata only and must never be opened.
    """
    raise NotImplementedError('complete the manifest summary')
