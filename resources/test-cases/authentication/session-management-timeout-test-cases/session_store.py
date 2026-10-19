"""Minimal session store that mirrors the TaskFlow rules from the resource.

Injectable clock so tests can simulate idle timeouts, absolute limits and
token expiry without sleeping. Not production code — a test lab.
"""

from __future__ import annotations

import secrets
import threading
from dataclasses import dataclass, field
from typing import Callable

IDLE_TIMEOUT_S = 30 * 60
ABSOLUTE_TIMEOUT_S = 8 * 60 * 60
ACCESS_TOKEN_TTL_S = 15 * 60

COOKIE_FLAGS = {"HttpOnly": True, "Secure": True, "SameSite": "Lax"}


@dataclass
class Session:
    session_id: str
    user: str
    access_token: str
    refresh_token: str
    created_at: float
    last_activity: float
    access_expires_at: float
    persistent: bool
    cookie_flags: dict = field(default_factory=lambda: dict(COOKIE_FLAGS))


class SessionError(Exception):
    pass


class SessionStore:
    """Redis-style server-side session store with sliding + absolute expiry."""

    def __init__(self, now: Callable[[], float]) -> None:
        self._now = now
        self._sessions: dict[str, Session] = {}
        self._revoked_refresh: set[str] = set()
        self._refresh_locks: dict[str, threading.Lock] = {}
        self._global_lock = threading.Lock()

    def login(self, user: str, remember_me: bool = False) -> Session:
        session = Session(
            session_id=secrets.token_hex(8),
            user=user,
            access_token=secrets.token_hex(8),
            refresh_token=secrets.token_hex(8),
            created_at=self._now(),
            last_activity=self._now(),
            access_expires_at=self._now() + ACCESS_TOKEN_TTL_S,
            persistent=remember_me,
        )
        self._sessions[session.session_id] = session
        return session

    def browser_restart_survives(self, session: Session) -> bool:
        """A browser restart only keeps persistent (remember-me) cookies."""
        return session.persistent

    def _expired(self, session: Session) -> bool:
        now = self._now()
        if now - session.created_at >= ABSOLUTE_TIMEOUT_S:
            return True
        return now - session.last_activity >= IDLE_TIMEOUT_S

    def validate(self, session_id: str) -> Session:
        session = self._sessions.get(session_id)
        if session is None or self._expired(session):
            raise SessionError("session expired or unknown")
        session.last_activity = self._now()
        return session

    def access_token_valid(self, token: str) -> bool:
        for session in self._sessions.values():
            if session.access_token == token:
                return self._now() < session.access_expires_at
        return False

    def refresh(self, refresh_token: str) -> Session:
        """Single-flight rotation: concurrent refreshes on the same token
        are serialized so exactly one wins and the others replay the result."""
        owner = next(
            (s for s in self._sessions.values() if s.refresh_token == refresh_token),
            None,
        )
        if refresh_token in self._revoked_refresh:
            raise SessionError("refresh token revoked")
        if owner is None:
            raise SessionError("unknown refresh token")

        lock = self._refresh_locks.setdefault(refresh_token, threading.Lock())
        with lock, self._global_lock:
            if refresh_token in self._revoked_refresh:
                raise SessionError("refresh token revoked")
            owner.access_token = secrets.token_hex(8)
            owner.access_expires_at = self._now() + ACCESS_TOKEN_TTL_S
            new_refresh = secrets.token_hex(8)
            self._revoked_refresh.add(refresh_token)
            owner.refresh_token = new_refresh
            return owner

    def logout(self, session_id: str) -> None:
        session = self._sessions.pop(session_id, None)
        if session is not None:
            self._revoked_refresh.add(session.refresh_token)

    def change_password(self, user: str) -> int:
        doomed = [sid for sid, s in self._sessions.items() if s.user == user]
        for sid in doomed:
            self.logout(sid)
        return len(doomed)

    def lockout(self, user: str) -> None:
        self.change_password(user)
