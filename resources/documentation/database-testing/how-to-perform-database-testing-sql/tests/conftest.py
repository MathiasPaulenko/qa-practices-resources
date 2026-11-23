import os

import psycopg2
import pytest


@pytest.fixture
def db_connection():
    """Connection to a dedicated test database.

    Placeholder defaults — point DB_* env vars at your own Postgres
    instance (a Docker container or a template database), never at
    production.
    """
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "testdb"),
        user=os.environ.get("DB_USER", "test"),
        password=os.environ.get("DB_PASSWORD", "test"),
    )
    yield conn
    conn.close()


@pytest.fixture
def seeded_users(db_connection):
    """Seed a minimal users/orders schema and clean it up afterwards."""
    cursor = db_connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            total NUMERIC(10, 2) NOT NULL
        )
        """
    )
    db_connection.commit()
    yield cursor
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS users")
    db_connection.commit()
    cursor.close()
