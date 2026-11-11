import requests

MOCK_BASE = "http://localhost:8080"


def test_get_user_uses_mock():
    response = requests.get(f"{MOCK_BASE}/users/123")
    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_unmapped_endpoint_returns_404():
    response = requests.get(f"{MOCK_BASE}/users/999")
    assert response.status_code == 404
