import pytest
import requests

BASE_URL = "https://sandbox.provider.example.com"
VALID_API_KEY = "sandbox-key-123"
INVALID_API_KEY = "invalid-key"
EXPIRED_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.expired"


def test_valid_api_key():
    headers = {"Authorization": f"Bearer {VALID_API_KEY}"}
    response = requests.get(f"{BASE_URL}/api/v1/account", headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()


def test_invalid_api_key():
    headers = {"Authorization": f"Bearer {INVALID_API_KEY}"}
    response = requests.get(f"{BASE_URL}/api/v1/account", headers=headers)
    assert response.status_code in (401, 403)
    assert "stack" not in response.text.lower()


def test_expired_token():
    headers = {"Authorization": f"Bearer {EXPIRED_TOKEN}"}
    response = requests.get(f"{BASE_URL}/api/v1/account", headers=headers)
    assert response.status_code in (401, 403)
