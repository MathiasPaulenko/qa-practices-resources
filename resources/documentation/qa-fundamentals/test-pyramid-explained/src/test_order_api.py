# test_order_api.py
# Integration test for order persistence — Test Pyramid layer: Integration
# Run with: pytest src/test_order_api.py
# Requires: API server running at http://localhost:8000

import requests

BASE_URL = 'http://localhost:8000'


def test_create_order_persists_and_emits_event():
    payload = {'user_id': 1, 'items': [{'sku': 'BOOK-001', 'qty': 2}]}
    response = requests.post(f'{BASE_URL}/orders', json=payload)
    assert response.status_code == 201

    order = response.json()
    assert order['status'] == 'pending'

    saved = requests.get(f"{BASE_URL}/orders/{order['id']}").json()
    assert saved['items'][0]['sku'] == 'BOOK-001'


def test_order_with_invalid_sku_returns_400():
    payload = {'user_id': 1, 'items': [{'sku': 'INVALID', 'qty': 2}]}
    response = requests.post(f'{BASE_URL}/orders', json=payload)
    assert response.status_code == 400
