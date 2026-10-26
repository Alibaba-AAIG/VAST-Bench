from __future__ import annotations

from threading import RLock


class SessionStore:
    def __init__(self):
        self._lock = RLock()
        self._active_sessions: set[str] = set()
        self._pending_logout: dict[str, str] = {}

    def add(self, session_id: str) -> None:
        with self._lock:
            self._active_sessions.add(session_id)

    def register_logout(self, request_id: str, session_id: str) -> None:
        with self._lock:
            if session_id not in self._active_sessions:
                raise KeyError(session_id)
            self._pending_logout[request_id] = session_id

    def complete_logout(self, request_id: str) -> bool:
        with self._lock:
            session_id = self._pending_logout.pop(request_id, None)
            if session_id is None:
                return False
            self._active_sessions.discard(session_id)
            return True

    def is_active(self, session_id: str) -> bool:
        with self._lock:
            return session_id in self._active_sessions
