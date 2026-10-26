"""Core indexing for notesd.

Builds a tiny in-memory index over note bodies and answers substring queries. Pure standard
library so the tool runs anywhere.
"""
from __future__ import annotations


def index_notes(notes: dict[str, str]) -> dict[str, list[str]]:
    """Map each lowercased word to the ids of notes that contain it."""
    index: dict[str, list[str]] = {}
    for note_id, body in notes.items():
        for word in {w.lower() for w in body.split()}:
            index.setdefault(word, []).append(note_id)
    return index


def search(index: dict[str, list[str]], term: str) -> list[str]:
    """Return the note ids matching a single search term."""
    return sorted(index.get(term.lower(), []))
