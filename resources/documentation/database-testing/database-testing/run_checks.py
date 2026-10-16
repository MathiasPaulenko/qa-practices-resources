"""Run the integrity checks from integrity_checks.sql against a SQLite DB.

Usage:
    python run_checks.py                 # in-memory DB with schema + seed
    python run_checks.py path/to.db      # existing database file

Exits 0 when every check reports 0 violations, 1 otherwise — so it can be
dropped into a CI job as-is.
"""

import sqlite3
import sys
from pathlib import Path

BASE = Path(__file__).parent


def split_statements(sql: str) -> list[str]:
    """Split the checks file into single SELECT statements."""
    return [s.strip() for s in sql.split(";") if "SELECT" in s.upper()]


def check_names(sql: str) -> list[str]:
    return [line.split("-- CHECK")[1].strip() for line in sql.splitlines() if "-- CHECK" in line]


def open_db(path: str | None = None) -> sqlite3.Connection:
    if path:
        return sqlite3.connect(path)
    db = sqlite3.connect(":memory:")
    db.executescript((BASE / "schema.sql").read_text())
    db.executescript((BASE / "seed.sql").read_text())
    return db


def main() -> int:
    db = open_db(sys.argv[1] if len(sys.argv) > 1 else None)
    sql = (BASE / "integrity_checks.sql").read_text()
    names = check_names(sql)
    statements = split_statements(sql)
    failures = 0
    for name, stmt in zip(names, statements):
        violations = db.execute(stmt).fetchone()[0]
        status = "OK" if violations == 0 else "FAIL"
        if violations:
            failures += 1
        print(f"[{status}] {name} — {violations} violation(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
