import requests

BASE = "https://staging.lumapay.com/api/v1"

headers = {"Authorization": "Bearer " + staging_token}

def test_create_order_returns_201():
    payload = {"product_id": "prd-48291", "quantity": 2}
    response = requests.post(f"{BASE}/orders", json=payload, headers=headers)
    assert response.status_code == 201
    assert "order_id" in response.json()

def test_rate_limit_returns_429():
    for _ in range(101):
        response = requests.get(f"{BASE}/products", headers=headers)
    assert response.status_code == 429
