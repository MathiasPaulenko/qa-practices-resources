"""TC-001 — API to database integration: POST via API, verify the row in the DB."""
import requests
import sqlite3

BASE = "http://localhost:8080"


def test_user_created_in_database():
    r = requests.post(f"{BASE}/api/users", json={"name": "Ada", "email": "ada@corp.io"})
    assert r.status_code == 201
    user_id = r.json()["id"]
    row = sqlite3.connect("app.db").execute(
        "SELECT email FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    assert row and row[0] == "ada@corp.io"
