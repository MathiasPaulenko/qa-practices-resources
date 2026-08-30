import pytest
import requests

BASE_URL = "https://sandbox.provider.example.com"
API_KEY = "sandbox-key-123"
RATE_LIMIT = 1000


def test_rate_limit_headers_and_429():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    # Send requests up to the limit
    for _ in range(RATE_LIMIT):
        requests.get(f"{BASE_URL}/api/v1/small", headers=headers)

    # The request over the limit should return 429
    response = requests.get(f"{BASE_URL}/api/v1/small", headers=headers)
    assert response.status_code == 429
    assert "Retry-After" in response.headers
