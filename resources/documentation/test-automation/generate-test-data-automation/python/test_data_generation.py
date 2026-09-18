"""Runnable examples for the test data generation guide.

Step 2 (Faker Python), Step 5 (database seeding via sqlite + yield fixture)
and Step 6 (CSV output) — all self-contained, no external services needed.
"""
import csv
import sqlite3

import pytest
from faker import Faker

fake = Faker()


def test_faker_produces_realistic_shapes():
    user = {
        "id": fake.uuid4(),
        "name": fake.name(),
        "email": fake.email(),
    }
    assert "@" in user["email"]
    assert len(user["id"]) == 36


def test_seed_makes_runs_deterministic():
    fake_a = Faker()
    fake_b = Faker()
    fake_a.seed_instance(12345)
    fake_b.seed_instance(12345)
    assert fake_a.name() == fake_b.name()


def test_localized_data():
    fake_es = Faker("es_ES")
    assert fake_es.name()  # non-empty Spanish-locale name


# --- Step 5: seeding with a real database (sqlite, stdlib) ---


@pytest.fixture(scope="function")
def seeded_db(tmp_path):
    """Seed an in-memory-like sqlite DB and clean up after the test."""
    conn = sqlite3.connect(tmp_path / "test.db")
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
    )
    local_fake = Faker()
    for _ in range(10):
        conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (local_fake.name(), local_fake.email()),
        )
    conn.commit()

    yield conn

    conn.execute("DELETE FROM users")
    conn.commit()
    conn.close()


def test_seeded_users_exist(seeded_db):
    count = seeded_db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    assert count == 10


def test_cleanup_after_fixture(seeded_db):
    """A second test re-seeds from scratch — no state leaks between tests."""
    emails = [
        row[0] for row in seeded_db.execute("SELECT email FROM users")
    ]
    assert all("@" in e for e in emails)


# --- Step 6: CSV output ---


def test_csv_generation(tmp_path):
    out = tmp_path / "test_users.csv"
    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "email", "phone", "city", "age"])
        for _ in range(100):
            writer.writerow(
                [
                    fake.name(),
                    fake.email(),
                    fake.phone_number(),
                    fake.city(),
                    fake.random_int(min=18, max=80),
                ]
            )

    rows = list(csv.reader(open(out)))
    assert rows[0] == ["name", "email", "phone", "city", "age"]
    assert len(rows) == 101
