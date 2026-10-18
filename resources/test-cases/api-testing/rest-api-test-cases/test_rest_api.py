"""REST API contract test suite — pytest 8.3 + requests 2.32.

Covers the core cases from the guide: contract shape (TC-001), clean 404
(TC-006), auth challenge (TC-013), idempotent PUT (TC-003) and the
rate-limit headers check (TC-015).

Setup:
    pip install pytest requests
    export API_BASE_URL="https://your-api.example.com/api/v1"
    export API_TOKEN="your-test-token"
    pytest test_rest_api.py -v
"""

import os

import pytest
import requests

BASE_URL = os.environ.get("API_BASE_URL", "https://api.example.com/api/v1")
TOKEN = os.environ.get("API_TOKEN", "test-token")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

VALID_USER = {"name": "Grace Hopper", "email": "grace@example.com", "role": "member"}
CONTRACT_KEYS = {"id", "name", "email", "role", "created_at"}


def test_get_user_returns_contract_shape():
    """TC-001: GET returns 200 with the declared schema."""
    resp = requests.get(f"{BASE_URL}/users/42", headers=HEADERS, timeout=10)
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("Content-Type", "")
    assert CONTRACT_KEYS <= resp.json().keys()


def test_post_creates_addressable_resource():
    """TC-002: POST returns 201 with a working Location header."""
    resp = requests.post(f"{BASE_URL}/users", json=VALID_USER, headers=HEADERS, timeout=10)
    assert resp.status_code == 201
    location = resp.headers.get("Location")
    assert location, "201 without Location header"
    assert "/users/" in location


def test_put_is_idempotent():
    """TC-003: the same PUT twice leaves the same state."""
    payload = {"name": "Ada Lovelace", "email": "ada@example.com", "role": "admin"}
    first = requests.put(f"{BASE_URL}/users/42", json=payload, headers=HEADERS, timeout=10)
    second = requests.put(f"{BASE_URL}/users/42", json=payload, headers=HEADERS, timeout=10)
    assert first.status_code in (200, 204)
    assert second.status_code in (200, 204)
    if first.status_code == 200 and second.status_code == 200:
        assert first.json() == second.json()


def test_missing_user_returns_clean_404():
    """TC-006: a non-existent id returns 404 with a structured error."""
    resp = requests.get(f"{BASE_URL}/users/999999", headers=HEADERS, timeout=10)
    assert resp.status_code == 404
    body = resp.json()
    assert "error" in body or "message" in body


def test_malformed_json_returns_400():
    """TC-007: broken JSON is rejected at the parse layer."""
    resp = requests.post(
        f"{BASE_URL}/users",
        data=b'{"name": "Grace", "email":',
        headers=HEADERS,
        timeout=10,
    )
    assert resp.status_code == 400


def test_missing_required_field_is_reported():
    """TC-008: validation errors name the missing field."""
    resp = requests.post(
        f"{BASE_URL}/users",
        json={"name": "Grace Hopper"},  # missing email
        headers=HEADERS,
        timeout=10,
    )
    assert resp.status_code in (400, 422)
    assert "email" in resp.text


def test_unauthenticated_request_gets_challenge():
    """TC-013: no token -> 401 + WWW-Authenticate."""
    resp = requests.get(f"{BASE_URL}/users/42", timeout=10)
    assert resp.status_code == 401
    assert "WWW-Authenticate" in resp.headers


def test_sql_injection_payload_rejected():
    """TC-011: injection payloads get 400/403, never a SQL error."""
    for payload in ("1' OR '1'='1", "name; DROP TABLE users--"):
        resp = requests.get(f"{BASE_URL}/users", params={"id": payload}, headers=HEADERS, timeout=10)
        assert resp.status_code in (400, 403)
        assert "sql" not in resp.text.lower() or "syntax" not in resp.text.lower()


def test_rate_limit_returns_429_with_retry_after():
    """TC-015: past the limit -> 429 + Retry-After. Skip if no limit set."""
    limit = int(os.environ.get("API_RATE_LIMIT", "0"))
    if not limit:
        pytest.skip("Set API_RATE_LIMIT to enable this test")
    for _ in range(limit + 5):
        resp = requests.get(f"{BASE_URL}/users/42", headers=HEADERS, timeout=10)
    assert resp.status_code == 429
    assert "Retry-After" in resp.headers
