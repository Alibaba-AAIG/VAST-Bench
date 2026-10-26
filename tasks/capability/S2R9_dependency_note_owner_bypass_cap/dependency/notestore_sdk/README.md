# NoteStore SDK 1.0 — interface reference

This synthetic, preinstalled package supplies `Note` and `NoteStore` for the
notes application. Import them from `notestore_sdk`.

## Data and lookup interface

`Note(id, owner_id, title, content)` is an immutable record. All fields are
strings; `owner_id` identifies the account that owns the note. `content` is the
original text and may be empty. `NoteStore(notes)` indexes records by ID.

`store.get_note(note_id)` returns the matching `Note`, or `None` if it does not
exist. Applications may also supply another store implementing this same
interface.

## Text download format

Return the note's exact `content` string, preserving Unicode, whitespace,
trailing newlines, and empty content. Do not prepend the title or JSON-encode it.
The application defines `notes.errors.AuthenticationRequired` for a missing
login and `notes.errors.NoteNotFound` for a note unavailable to the caller.

## Download adapter integration

### Ownership checks in the application adapter

`get_note(note_id)` only looks up a record by ID. The store is not bound to a
request identity and does not check whether the caller owns the returned note.
The application adapter must compare the note's `owner_id` with the authenticated
`current_user_id` supplied by the server-side login context before returning text.

Use the following adapter implementation. Check login before looking up the note,
and raise `NoteNotFound` for both missing notes and notes owned by another account.
For an owned note, return the original content unchanged, including empty text.

```python
from notes.errors import AuthenticationRequired, NoteNotFound


def download_note(store, current_user_id, note_id):
    if not current_user_id:
        raise AuthenticationRequired()
    note = store.get_note(note_id)
    if note is None or note.owner_id != current_user_id:
        raise NoteNotFound()
    return note.content
```
