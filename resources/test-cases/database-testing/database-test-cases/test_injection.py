"""Parameterized-query check for database-test-cases.

Runs against an in-memory SQLite database so it needs no server — the
principle is identical on PostgreSQL: the payload must be bound as a
parameter, never interpolated into the SQL string.

Requires: Python 3.10+, pytest 8.3 (`pip install pytest`)
Run:      pytest test_injection.py -v
"""

import sqlite3

import pytest


def get_users(search: str, conn: sqlite3.Connection):
    """Safe implementation: binds `search` as a parameter."""
    cur = conn.execute(
        "SELECT id, name, email FROM users WHERE email = ?", (search,)
    )
    return cur.fetchall()


def get_users_unsafe(search: str, conn: sqlite3.Connection):
    """Deliberately vulnerable implementation — for contrast only."""
    cur = conn.execute(
        f"SELECT id, name, email FROM users WHERE email = '{search}'"
    )
    return cur.fetchall()


@pytest.fixture()
def conn():
    c = sqlite3.connect(":memory:")
    c.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE)"
    )
    c.execute(
        "INSERT INTO users (id, name, email) VALUES "
        "(42, 'Ingrid Bergström', 'ingrid.bergstrom@example.com'), "
        "(99, 'Tariq Mahmoud', 'tariq.mahmoud@example.com'), "
        "(7, 'Ana Gómez', 'ana.gomez@example.com')"
    )
    yield c
    c.close()


PAYLOAD = "' OR '1'='1"


def test_parameterized_query_resists_injection(conn):
    """TC-021: the payload is treated as a literal string, not SQL."""
    rows = get_users(search=PAYLOAD, conn=conn)
    # no user has this email — the payload must not match everything
    assert rows == []


def test_vulnerable_version_would_leak_rows(conn):
    """Contrast check: interpolation actually returns all users."""
    rows = get_users_unsafe(search=PAYLOAD, conn=conn)
    assert len(rows) == 3  # proves the payload works if unparameterized


def test_legitimate_lookup_still_works(conn):
    rows = get_users(search="ingrid.bergstrom@example.com", conn=conn)
    assert len(rows) == 1
    assert rows[0][1] == "Ingrid Bergström"
