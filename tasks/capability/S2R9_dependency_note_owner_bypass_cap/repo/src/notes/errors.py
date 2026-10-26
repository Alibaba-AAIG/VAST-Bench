class AuthenticationRequired(Exception):
    """The caller has no authenticated server-side identity."""


class NoteNotFound(Exception):
    """The note is unavailable to this caller."""
