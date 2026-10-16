"""Runnable demos of transaction testing against SQLite (stdlib only).

Each demo maps to a section of the guide:
  1. Atomicity   — a mid-transaction failure rolls back the first write
  2. Savepoints  — partial rollback keeps earlier work
  3. Optimistic locking — a version-mismatched write is rejected
  4. Implicit rollback — closing a connection mid-transaction discards changes
  5. Consistency — CHECK constraint blocks a negative balance
"""
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent


def fresh_db() -> sqlite3.Connection:
    db_path = HERE / "demo.db"
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript((HERE / "schema.sql").read_text())
    conn.executescript((HERE / "seed.sql").read_text())
    return conn


def balances(conn) -> dict:
    return dict(conn.execute("SELECT id, balance FROM accounts").fetchall())


def transfer(conn, from_id, to_id, amount):
    """Multi-step write: debit + credit + audit row. Must be all-or-nothing."""
    conn.execute("BEGIN")
    conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?",
                 (amount, from_id))
    conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?",
                 (amount, to_id))
    conn.execute("INSERT INTO transfers (from_id, to_id, amount) VALUES (?,?,?)",
                 (from_id, to_id, amount))
    conn.execute("COMMIT")


def demo_atomicity(conn):
    """Fail mid-transaction: the debit must not survive."""
    try:
        conn.execute("BEGIN")
        conn.execute("UPDATE accounts SET balance = balance - 50 WHERE id = 1")
        raise RuntimeError("simulated application crash")  # in-app failure
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
    assert balances(conn) == {1: 100, 2: 100}, "atomicity broken"
    print("1. atomicity: mid-transaction failure left no partial write")


def demo_savepoint(conn):
    """ROLLBACK TO SAVEPOINT undoes the fee, keeps the insert."""
    conn.execute("BEGIN")
    conn.execute("INSERT INTO accounts (id, owner, balance) VALUES (3, 'carol', 10)")
    conn.execute("SAVEPOINT before_fee")
    conn.execute("UPDATE accounts SET balance = balance - 5 WHERE id = 3")
    conn.execute("ROLLBACK TO SAVEPOINT before_fee")
    conn.execute("COMMIT")
    row = conn.execute("SELECT balance FROM accounts WHERE id = 3").fetchone()
    assert row[0] == 10, "savepoint rollback failed"
    print("2. savepoint: partial rollback kept the insert, undid the fee")


def demo_optimistic_lock(conn):
    """A write with a stale version is rejected — no lost update."""
    row = conn.execute("SELECT balance, version FROM accounts WHERE id = 1").fetchone()
    stale_version = row[1]
    conn.execute("UPDATE accounts SET version = version + 1 WHERE id = 1")  # someone else wrote
    cur = conn.execute(
        "UPDATE accounts SET balance = ?, version = version + 1 "
        "WHERE id = 1 AND version = ?",
        (row[0] + 25, stale_version),
    )
    assert cur.rowcount == 0, "stale write was applied"
    conn.execute("COMMIT")
    print("3. optimistic locking: stale version rejected the second write")


def demo_implicit_rollback(conn):
    """Closing a connection mid-transaction rolls back silently."""
    conn.execute("BEGIN")
    conn.execute("UPDATE accounts SET balance = 0 WHERE id = 2")
    conn.close()  # no COMMIT
    conn2 = sqlite3.connect(HERE / "demo.db")
    b = conn2.execute("SELECT balance FROM accounts WHERE id = 2").fetchone()[0]
    conn2.close()
    assert b == 100, "implicit rollback failed"
    print("4. implicit rollback: uncommitted write vanished on disconnect")


def demo_consistency(conn):
    """CHECK constraint rejects a negative balance inside the transaction."""
    try:
        transfer(conn, 1, 2, 500)
    except sqlite3.IntegrityError:
        pass  # constraint fired — whole transaction aborted
    assert balances(conn) == {1: 100, 2: 100}, "consistency broken"
    print("5. consistency: CHECK rejected the overdraft, no partial state")


if __name__ == "__main__":
    conn = fresh_db()
    try:
        demo_atomicity(conn)
        demo_savepoint(conn)
        demo_optimistic_lock(conn)
        demo_implicit_rollback(conn)
        conn = fresh_db()
        demo_consistency(conn)
    finally:
        conn.close()
    print("\nAll transaction demos passed.")
