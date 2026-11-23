def test_cascade_delete(seeded_users):
    cursor = seeded_users
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
        ("Cascade Test", "cascade@example.com"),
    )
    user_id = cursor.fetchone()[0]

    cursor.execute(
        "INSERT INTO orders (user_id, total) VALUES (%s, %s)", (user_id, 50.00)
    )

    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

    cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
    assert cursor.fetchone() is None


def test_transaction_rollback(seeded_users):
    cursor = seeded_users
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
        ("Rollback Test", "rollback@example.com"),
    )
    user_id = cursor.fetchone()[0]

    cursor.connection.rollback()

    # Rolled back: fixture seed survives, the user insert does not.
    cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    assert cursor.fetchone() is None
