"""Tests mapping to the session management test cases (TC-001..TC-030)."""

import threading

import pytest

from session_store import (
    ACCESS_TOKEN_TTL_S,
    ABSOLUTE_TIMEOUT_S,
    IDLE_TIMEOUT_S,
    SessionError,
    SessionStore,
)


class FakeClock:
    def __init__(self) -> None:
        self.t = 1_000_000.0

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


@pytest.fixture()
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture()
def store(clock: FakeClock) -> SessionStore:
    return SessionStore(now=clock)


def test_idle_timeout_expires_at_30_minutes(store: SessionStore, clock: FakeClock) -> None:
    """TC-001: session dies exactly at the idle boundary."""
    session = store.login("alice@taskflow.io")
    clock.advance(IDLE_TIMEOUT_S - 60)
    assert store.validate(session.session_id) is session
    clock.advance(IDLE_TIMEOUT_S + 1)
    with pytest.raises(SessionError):
        store.validate(session.session_id)


def test_activity_resets_idle_timer(store: SessionStore, clock: FakeClock) -> None:
    """TC-002/TC-009: sliding expiration keeps active sessions alive."""
    session = store.login("alice@taskflow.io")
    for _ in range(6):
        clock.advance(10 * 60)
        store.validate(session.session_id)
    assert session.last_activity == clock.t


def test_refresh_issues_new_access_token(store: SessionStore) -> None:
    """TC-003: refresh rotates the access token."""
    session = store.login("alice@taskflow.io")
    old_access, old_refresh = session.access_token, session.refresh_token
    store.refresh(old_refresh)
    assert session.access_token != old_access
    assert session.refresh_token != old_refresh


def test_remember_me_survives_browser_restart(store: SessionStore) -> None:
    """TC-004: persistent cookie keeps the session across a restart."""
    session = store.login("alice@taskflow.io", remember_me=True)
    assert store.browser_restart_survives(session)


def test_no_remember_me_dies_on_browser_restart(store: SessionStore) -> None:
    """TC-005: a session cookie dies with the browser."""
    session = store.login("alice@taskflow.io", remember_me=False)
    assert not store.browser_restart_survives(session)


def test_concurrent_sessions_same_user(store: SessionStore) -> None:
    """TC-006: TaskFlow's policy allows two browsers on one account."""
    a = store.login("alice@taskflow.io")
    b = store.login("alice@taskflow.io")
    assert store.validate(a.session_id) is a
    assert store.validate(b.session_id) is b


def test_logout_invalidates_session(store: SessionStore) -> None:
    """TC-008: logout destroys the session server-side."""
    session = store.login("alice@taskflow.io")
    store.logout(session.session_id)
    with pytest.raises(SessionError):
        store.validate(session.session_id)


def test_absolute_timeout_ignores_activity(store: SessionStore, clock: FakeClock) -> None:
    """TC-010: the 8h cap kills even a continuously active session."""
    session = store.login("alice@taskflow.io")
    while clock.t - session.created_at < ABSOLUTE_TIMEOUT_S - 1500:
        clock.advance(20 * 60)
        store.validate(session.session_id)
    clock.advance(ABSOLUTE_TIMEOUT_S + 1 - (clock.t - session.created_at))
    with pytest.raises(SessionError):
        store.validate(session.session_id)


def test_expired_access_token_rejected(store: SessionStore, clock: FakeClock) -> None:
    """TC-012: an access token past its 15-minute TTL is rejected."""
    session = store.login("alice@taskflow.io")
    assert store.access_token_valid(session.access_token)
    clock.advance(ACCESS_TOKEN_TTL_S + 1)
    assert not store.access_token_valid(session.access_token)


def test_revoked_refresh_token_rejected(store: SessionStore) -> None:
    """TC-013: logout revokes the refresh token."""
    session = store.login("alice@taskflow.io")
    refresh = session.refresh_token
    store.logout(session.session_id)
    with pytest.raises(SessionError):
        store.refresh(refresh)


def test_login_regenerates_session_id(store: SessionStore) -> None:
    """TC-014: every login mints a fresh session ID (fixation defense)."""
    first = store.login("attacker@taskflow.io")
    second = store.login("alice@taskflow.io")
    assert first.session_id != second.session_id


def test_password_change_kills_all_sessions(store: SessionStore) -> None:
    """TC-022: a password change invalidates every session of the user."""
    a = store.login("alice@taskflow.io")
    b = store.login("alice@taskflow.io")
    assert store.change_password("alice@taskflow.io") == 2
    for session in (a, b):
        with pytest.raises(SessionError):
            store.validate(session.session_id)


def test_single_flight_refresh_under_concurrency(store: SessionStore) -> None:
    """TC-028: concurrent refreshes produce exactly one new token, no stampede."""
    session = store.login("alice@taskflow.io")
    old_refresh = session.refresh_token
    results: list[object] = []
    errors: list[Exception] = []

    def call() -> None:
        try:
            results.append(store.refresh(old_refresh))
        except SessionError as exc:
            errors.append(exc)

    threads = [threading.Thread(target=call) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(results) == 1
    assert len(errors) == 4
    assert session.refresh_token != old_refresh
    with pytest.raises(SessionError):
        store.refresh(old_refresh)


def test_lockout_kills_active_session(store: SessionStore) -> None:
    """TC-029: an account lockout terminates the live session."""
    session = store.login("alice@taskflow.io")
    store.lockout("alice@taskflow.io")
    with pytest.raises(SessionError):
        store.validate(session.session_id)


def test_session_cookie_flags(store: SessionStore) -> None:
    """TC-016/017/018: the session cookie carries Secure, HttpOnly, SameSite."""
    session = store.login("alice@taskflow.io")
    assert session.cookie_flags == {
        "HttpOnly": True,
        "Secure": True,
        "SameSite": "Lax",
    }
