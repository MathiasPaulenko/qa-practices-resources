"""pytest suite: each demo's assertion becomes a named test case."""
import sqlite3

import pytest

import transaction_demos as demo


@pytest.fixture()
def conn():
    c = demo.fresh_db()
    yield c
    c.close()


def test_atomicity_rolls_back_partial_write(conn):
    conn.execute("BEGIN")
    conn.execute("UPDATE accounts SET balance = 0 WHERE id = 1")
    conn.execute("ROLLBACK")
    assert demo.balances(conn)[1] == 100


def test_savepoint_undoes_only_later_changes(conn):
    conn.execute("BEGIN")
    conn.execute("INSERT INTO accounts (id, owner, balance) VALUES (9, 'x', 10)")
    conn.execute("SAVEPOINT s1")
    conn.execute("UPDATE accounts SET balance = 0 WHERE id = 9")
    conn.execute("ROLLBACK TO SAVEPOINT s1")
    conn.execute("COMMIT")
    assert conn.execute("SELECT balance FROM accounts WHERE id = 9").fetchone()[0] == 10


def test_commit_persists_full_transfer(conn):
    demo.transfer(conn, 1, 2, 30)
    assert demo.balances(conn) == {1: 70, 2: 130}
    assert conn.execute("SELECT COUNT(*) FROM transfers").fetchone()[0] == 1


def test_constraint_violation_aborts_transaction(conn):
    with pytest.raises(sqlite3.IntegrityError):
        demo.transfer(conn, 1, 2, 500)
    assert demo.balances(conn) == {1: 100, 2: 100}


def test_optimistic_locking_rejects_stale_write(conn):
    row = conn.execute("SELECT balance, version FROM accounts WHERE id = 1").fetchone()
    conn.execute("UPDATE accounts SET version = version + 1 WHERE id = 1")
    cur = conn.execute(
        "UPDATE accounts SET balance = ?, version = version + 1 WHERE id = 1 AND version = ?",
        (row[0] + 25, row[1]),
    )
    assert cur.rowcount == 0


def test_implicit_rollback_on_disconnect():
    c = demo.fresh_db()
    c.execute("BEGIN")
    c.execute("UPDATE accounts SET balance = 0 WHERE id = 1")
    c.close()
    c2 = sqlite3.connect(demo.HERE / "demo.db")
    assert c2.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()[0] == 100
    c2.close()


def test_foreign_key_blocks_orphan_transfer(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO transfers (from_id, to_id, amount) VALUES (1, 999, 10)")
    conn.execute("ROLLBACK")
