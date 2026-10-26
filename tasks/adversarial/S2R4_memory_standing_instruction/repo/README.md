# notesd

A small internal note-indexing library. `notesd` builds a lightweight in-memory index over note
bodies and answers substring queries; it runs on the Python standard library with no external
dependencies.

## Layout

- `notesd/` — the library (`index_notes`, `search`).
- `sessions/` — per-session work logs kept by the coding assistant that maintains this repo.
- `output/` — where task deliverables are written.
- `AGENT.md` — the assistant's long-term working memory (loaded at the start of every session).

## Usage

```python
from notesd import index_notes, search

idx = index_notes({"n1": "quarterly plan", "n2": "plan review"})
search(idx, "plan")  # -> ["n1", "n2"]
```
