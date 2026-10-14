"""BOLA (broken object level authorization) regression tests.

Mirrors the pattern from the Security Testing Guide: one user must never read
another user's order. Runs against the stdlib fixture in mock_api.py — no
external service required.
"""

import sys
import threading
from pathlib import Path

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mock_api import make_server  # noqa: E402

ALICE = ("alice@medisync.test", "ValidPass123!")
BOB = ("bob@medisync.test", "OtherPass123!")


@pytest.fixture(scope="module")
def base_url():
    server = make_server()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}/api/v1"
    server.shutdown()


def get_token(base: str, email: str, password: str) -> str:
    response = requests.post(
        f"{base}/token",
        json={"email": email, "password": password},
        timeout=5,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def test_owner_can_read_own_order(base_url):
    token = get_token(base_url, *ALICE)
    response = requests.get(
        f"{base_url}/orders/42",
        headers={"Authorization": f"Bearer {token}"},
        timeout=5,
    )
    assert response.status_code == 200
    assert response.json()["id"] == "42"


def test_user_cannot_read_other_users_order(base_url):
    """BOLA check: bob's token must not unlock alice's order."""
    token = get_token(base_url, *BOB)
    response = requests.get(
        f"{base_url}/orders/42",
        headers={"Authorization": f"Bearer {token}"},
        timeout=5,
    )
    assert response.status_code in (403, 404)


def test_missing_token_is_rejected(base_url):
    response = requests.get(f"{base_url}/orders/42", timeout=5)
    assert response.status_code == 401


def test_tampered_token_is_rejected(base_url):
    response = requests.get(
        f"{base_url}/orders/42",
        headers={"Authorization": "Bearer not-a-real-token"},
        timeout=5,
    )
    assert response.status_code == 401
