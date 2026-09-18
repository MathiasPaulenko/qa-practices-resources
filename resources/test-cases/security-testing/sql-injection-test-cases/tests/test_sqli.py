"""SQLi payload verification for the SQL Injection Test Cases companion.

Each test maps to a case from the resource: it runs the same payload against
the intentionally vulnerable endpoint and the parameterized one, and asserts
the observable difference a tester should look for.
"""

import pytest

from app import app


@pytest.fixture()
def client():
    return app.test_client()


# --- TC-SQLI-001: classic error/auth-bypass login injection ------------------


def test_normal_login_works_on_both_endpoints(client):
    credentials = {"username": "admin", "password": "s3cr3t-admin-hash"}
    for endpoint in ("/vulnerable/login", "/secure/login"):
        response = client.post(endpoint, data=credentials)
        assert response.status_code == 200
        assert response.get_json()["user"] == "admin"


def test_vulnerable_login_bypassed_by_classic_payload(client):
    response = client.post(
        "/vulnerable/login",
        data={"username": "' OR '1'='1'--", "password": "whatever"},
    )
    # Vulnerable behavior: the OR clause makes the WHERE true for the first row,
    # and -- comments out the password check. A bare ' OR '1'='1 does NOT bypass:
    # AND binds tighter than OR, so the password clause still has to hold.
    assert response.status_code == 200
    assert response.get_json()["user"] == "admin"


def test_vulnerable_login_naive_payload_does_not_bypass(client):
    response = client.post(
        "/vulnerable/login",
        data={"username": "' OR '1'='1", "password": "whatever"},
    )
    # Verified by running it: '1'='1' AND password='whatever' is false, so the
    # whole OR branch is false and the row is not returned.
    assert response.status_code == 401


def test_secure_login_treats_payload_as_literal(client):
    response = client.post(
        "/secure/login",
        data={"username": "' OR '1'='1", "password": "whatever"},
    )
    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid credentials"


# --- TC-SQLI-002: UNION-based exfiltration in the search parameter -----------


UNION_PAYLOAD = "x' UNION SELECT username, password, email FROM users--"


def test_vulnerable_search_allows_union_exfiltration(client):
    response = client.get("/vulnerable/products", query_string={"category": UNION_PAYLOAD})
    rows = response.get_json()["products"]
    flat = str(rows)
    # Vulnerable behavior: user credentials leak into the product listing.
    assert "admin" in flat
    assert "s3cr3t-admin-hash" in flat


def test_secure_search_treats_union_as_literal(client):
    response = client.get("/secure/products", query_string={"category": UNION_PAYLOAD})
    assert response.get_json()["products"] == []


# --- Edge table: unquoted numeric parameter coercion -------------------------


def test_vulnerable_numeric_param_returns_all_rows(client):
    response = client.get("/vulnerable/product", query_string={"id": "1 OR 1=1"})
    # Vulnerable behavior: id=1 OR 1=1 evaluates the whole products table.
    assert len(response.get_json()["products"]) == 3


def test_secure_numeric_param_rejects_expression(client):
    response = client.get("/secure/product", query_string={"id": "1 OR 1=1"})
    assert response.get_json()["products"] == []
