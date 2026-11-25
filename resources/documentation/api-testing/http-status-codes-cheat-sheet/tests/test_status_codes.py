"""Status code contract tests for the HTTP status codes cheat sheet.

Covers the common matrix from the guide: happy path, client errors,
auth boundaries and rate limiting. Requires Python 3.10+, pytest 8.x
and requests 2.32.

Run:
    BASE_URL=https://staging.qapractices.com pytest tests/test_status_codes.py -v
"""

import os

import pytest
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:3000")
TOKEN = os.environ.get("API_TOKEN", "")


@pytest.fixture(scope="session")
def api() -> requests.Session:
    session = requests.Session()
    if TOKEN:
        session.headers["Authorization"] = f"Bearer {TOKEN}"
    return session


def test_get_existing_returns_200(api: requests.Session) -> None:
    response = api.get(f"{BASE_URL}/users/1", timeout=10)
    assert response.status_code == 200
    assert response.json()  # body is not empty on 200


def test_post_creates_returns_201_with_location(api: requests.Session) -> None:
    payload = {"email": "qa-status-codes@qapractices.com", "name": "QA"}
    response = api.post(f"{BASE_URL}/users", json=payload, timeout=10)
    assert response.status_code == 201
    assert "/users/" in response.headers.get("Location", "")


def test_delete_returns_204_then_404(api: requests.Session) -> None:
    created = api.post(
        f"{BASE_URL}/users",
        json={"email": "qa-delete@qapractices.com", "name": "QA"},
        timeout=10,
    )
    location = created.headers["Location"]
    delete = api.delete(f"{BASE_URL}{location}", timeout=10)
    assert delete.status_code == 204
    assert api.get(f"{BASE_URL}{location}", timeout=10).status_code == 404


def test_missing_auth_returns_401() -> None:
    response = requests.get(f"{BASE_URL}/users", timeout=10)
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers


def test_wrong_role_returns_403(api: requests.Session) -> None:
    assert api.get(f"{BASE_URL}/admin", timeout=10).status_code == 403


def test_invalid_payload_returns_422(api: requests.Session) -> None:
    response = api.post(
        f"{BASE_URL}/users", json={"email": "not-an-email"}, timeout=10
    )
    assert response.status_code == 422


def test_malformed_json_returns_400(api: requests.Session) -> None:
    response = api.post(
        f"{BASE_URL}/users",
        data="{invalid json",
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    assert response.status_code == 400


def test_unsupported_method_returns_405(api: requests.Session) -> None:
    response = api.patch(f"{BASE_URL}/users", json={}, timeout=10)
    assert response.status_code == 405
    assert "Allow" in response.headers


def test_rate_limit_returns_429_with_retry_after(api: requests.Session) -> None:
    codes = [
        api.get(f"{BASE_URL}/users", timeout=10).status_code
        for _ in range(150)
    ]
    assert 429 in codes
    last = api.get(f"{BASE_URL}/users", timeout=10)
    if last.status_code == 429:
        assert "Retry-After" in last.headers
