from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: str
    owner_id: str
    title: str
    content: str


class NoteStore:
    def __init__(self, notes):
        self._notes = {note.id: note for note in notes}

    def get_note(self, note_id):
        return self._notes.get(note_id)
