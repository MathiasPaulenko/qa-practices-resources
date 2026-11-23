def test_create_user(seeded_users):
    cursor = seeded_users
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
        ("John Doe", "john@example.com"),
    )
    user_id = cursor.fetchone()[0]

    cursor.execute("SELECT name, email FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    assert result == ("John Doe", "john@example.com")


def test_update_user(seeded_users):
    cursor = seeded_users
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
        ("Jane", "jane@example.com"),
    )
    user_id = cursor.fetchone()[0]

    cursor.execute(
        "UPDATE users SET name = %s WHERE id = %s", ("Jane Updated", user_id)
    )

    cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
    assert cursor.fetchone()[0] == "Jane Updated"
