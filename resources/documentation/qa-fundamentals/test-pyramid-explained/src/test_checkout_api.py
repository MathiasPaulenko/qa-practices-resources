# test_checkout_api.py
# API / Service test for checkout validation — Test Pyramid layer: API
# Run with: pytest src/test_checkout_api.py
# Requires: API server running at http://localhost:8000

import requests


def test_checkout_rejects_expired_payment_method():
    payload = {
        'email': 'qa@qapractices.com',
        'payment_token': 'tok_expired',
        'items': [{'sku': 'BOOK-001', 'qty': 1}]
    }
    response = requests.post('http://localhost:8000/checkout', json=payload)
    assert response.status_code == 422
    assert response.json()['field'] == 'payment_token'


def test_checkout_rejects_invalid_email():
    payload = {
        'email': 'not-an-email',
        'payment_token': 'tok_valid',
        'items': [{'sku': 'BOOK-001', 'qty': 1}]
    }
    response = requests.post('http://localhost:8000/checkout', json=payload)
    assert response.status_code == 422
    assert response.json()['field'] == 'email'
