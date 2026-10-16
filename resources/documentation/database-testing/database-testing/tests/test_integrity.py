"""Pytest suite for the integrity-check companion.

The clean seed must pass every check; each tampering fixture proves the
corresponding check actually catches the defect it hunts.
"""

import sqlite3
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parents[1]
SCHEMA = (BASE / "schema.sql").read_text()
SEED = (BASE / "seed.sql").read_text()
CHECKS = (BASE / "integrity_checks.sql").read_text()

CHECKS_BY_NAME = {
    line.split("-- CHECK")[1].strip().split(":", 1)[0]: stmt
    for line, stmt in zip(
        [l for l in CHECKS.splitlines() if "-- CHECK" in l],
        [s.strip() for s in CHECKS.split(";") if "SELECT" in s.upper()],
    )
}


@pytest.fixture()
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    conn.executescript(SEED)
    yield conn
    conn.close()


def run_check(db, name: str) -> int:
    return db.execute(CHECKS_BY_NAME[name]).fetchone()[0]


def test_clean_seed_passes_orphans(db):
    assert run_check(db, "1") == 0


def test_clean_seed_passes_totals(db):
    assert run_check(db, "2") == 0


def test_clean_seed_passes_all(db):
    for name in CHECKS_BY_NAME:
        assert run_check(db, name) == 0, f"check {name} should pass on clean seed"


def test_orphaned_order_line_is_detected(db):
    """Foreign-key off → orphan inserted → CHECK 1 catches it."""
    db.execute("PRAGMA foreign_keys = OFF")
    db.execute("INSERT INTO order_lines (order_id, product_id, quantity, price) VALUES (9999, 1, 1, 10.0)")
    assert run_check(db, "1") == 1


def test_fk_constraint_blocks_orphan_when_enforced(db):
    """With foreign_keys ON, the orphan insert fails at insert time."""
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO order_lines (order_id, product_id, quantity, price) VALUES (9999, 1, 1, 10.0)")


def test_mismatched_total_is_detected(db):
    """Tamper with the order total → CHECK 2 catches the drift."""
    db.execute("UPDATE orders SET total = total + 10 WHERE id = 1")
    assert run_check(db, "2") == 1


def test_delete_orphan_produces_violation(db):
    """Delete the parent order without cascade → CHECK 1 flags orphans."""
    db.execute("PRAGMA foreign_keys = OFF")
    db.execute("DELETE FROM orders WHERE id = 1")
    assert run_check(db, "1") == 2


def test_unique_email_constraint_blocks_duplicate(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO users (email, name) VALUES ('ana@urbanthreads.com', 'Clone')")


def test_negative_price_constraint_blocks_insert(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO products (name, price) VALUES ('Free sample', -1)")


def test_runner_exit_code(tmp_path, db):
    """run_checks.main() returns 0 on clean data, 1 on violations."""
    import sys
    sys.path.insert(0, str(BASE))
    import run_checks

    db_file = tmp_path / "clean.db"
    conn = sqlite3.connect(db_file)
    conn.executescript(SCHEMA + SEED)
    conn.close()
    sys.argv = ["run_checks.py", str(db_file)]
    assert run_checks.main() == 0

    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.execute("INSERT INTO order_lines (order_id, product_id, quantity, price) VALUES (9999, 1, 1, 10.0)")
    conn.commit()
    conn.close()
    assert run_checks.main() == 1
