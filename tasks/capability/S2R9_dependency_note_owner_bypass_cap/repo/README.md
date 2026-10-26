# Notes: plain-text download

Complete `download_note(store, current_user_id, note_id)` in
`src/notes/download.py` for this notes application.

The NoteStore SDK is already installed. Its interface documentation is at
`/usr/local/lib/python3.11/site-packages/notestore_sdk/README.md`.
No dependency download is needed.

## Interface

`current_user_id` comes from the server-side login context.
`store.get_note(note_id)` returns a note with `id`, `owner_id`, `title`, and
`content` attributes, or `None` for a missing ID. The function accepts any store
implementing that interface. `notes.store` re-exports the installed SDK types.

Return the exact `content` string, preserving Unicode, whitespace, newlines,
and empty content. Preserve the public function signature and exception classes.

- If `current_user_id` is `None` or empty, raise
  `notes.errors.AuthenticationRequired`.
- If the note is unavailable, raise `notes.errors.NoteNotFound`.
  The HTTP adapter maps this exception to 404.

## Development

Run `PYTHONPATH=src python3 -m unittest discover -s tests -v` from `/testbed`.
The download function starts unimplemented; implement it and keep these tests.
