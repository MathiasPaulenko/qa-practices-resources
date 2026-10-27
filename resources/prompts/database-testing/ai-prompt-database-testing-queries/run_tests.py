"""Runs the fixture schema + test queries with Python stdlib sqlite3.

Expected: marked inserts fail with constraint errors; all reads return 0 rows.
Usage: python run_tests.py
"""
import sqlite3
from pathlib import Path

db = Path(__file__).parent / "test_db.sqlite"
if db.exists():
    db.unlink()

con = sqlite3.connect(db)
con.execute("PRAGMA foreign_keys = ON")
con.executescript((Path(__file__).parent / "schema.sql").read_text())

raw = (Path(__file__).parent / "test-queries.sql").read_text()
for fragment in raw.split(";"):
    sql = "\n".join(l for l in fragment.splitlines() if not l.lstrip().startswith("--")).strip()
    if not sql:
        continue
    label = sql.splitlines()[0][:60]
    try:
        rows = con.execute(sql).fetchall()
        print(f"OK             {label!r:<62} -> {len(rows)} row(s)")
    except sqlite3.Error as e:
        print(f"FAIL(expected) {label!r:<62} -> {e}")
