import psycopg2
import pytest


def test_unique_constraint(seeded_users):
    cursor = seeded_users
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        ("User 1", "duplicate@example.com"),
    )

    with pytest.raises(psycopg2.IntegrityError):
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            ("User 2", "duplicate@example.com"),
        )


def test_not_null_constraint(seeded_users):
    cursor = seeded_users
    with pytest.raises(psycopg2.IntegrityError):
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, NULL)", ("No Email",)
        )


def test_foreign_key_constraint(seeded_users):
    cursor = seeded_users
    with pytest.raises(psycopg2.IntegrityError):
        cursor.execute(
            "INSERT INTO orders (user_id, total) VALUES (%s, %s)", (99999, 100.00)
        )
