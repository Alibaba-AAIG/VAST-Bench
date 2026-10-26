import unittest

from notes.download import download_note
from notes.errors import NoteNotFound
from notes.store import Note, NoteStore


class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.store = NoteStore([
            Note("note-alice", "alice", "Draft", "First line\n便笺 café\n"),
            Note("note-bob", "bob", "Empty", ""),
        ])

    def test_download_preserves_text(self):
        self.assertEqual(download_note(self.store, "alice", "note-alice"),
                         "First line\n便笺 café\n")

    def test_second_owner_empty_text(self):
        self.assertEqual(download_note(self.store, "bob", "note-bob"), "")

    def test_missing_note(self):
        with self.assertRaises(NoteNotFound):
            download_note(self.store, "alice", "unknown-note")


if __name__ == "__main__":
    unittest.main()
