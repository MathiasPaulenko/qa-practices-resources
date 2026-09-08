# tests/test_price_calc.py
# Requires: Python 3.12, pytest 8.3, requests 2.32
"""Test cart price calculations: subtotal, discount, tax and grand total."""
import pytest
import requests

BASE_URL = "https://staging.qa.local/api"


def test_tc04_subtotal_discount_tax_grand_total():
    """TC-04: Validate subtotal, discount, tax and grand total."""
    response = requests.post(
        f"{BASE_URL}/cart/calculate",
        json={
            "items": [
                {"sku": "SKU-A", "price": 29.99, "quantity": 1},
                {"sku": "SKU-B", "price": 15.00, "quantity": 1},
            ],
            "promo_code": "SAVE10",
            "shipping_zip": "90210",
        },
        timeout=10,
    )
    assert response.status_code == 200
    data = response.json()

    # Subtotal = 29.99 + 15.00 = 44.99
    assert data["subtotal"] == 44.99
    # Discount = 10% of 44.99 = 4.499 -> rounded to 4.50
    assert data["discount"] == -4.50
    # Tax = 8% of (44.99 - 4.50) = 8% of 40.49 = 3.2392 -> rounded to 3.24
    assert data["tax"] == 3.24
    # Shipping = 5.00
    assert data["shipping"] == 5.00
    # Grand total = 44.99 - 4.50 + 3.24 + 5.00 = 48.73
    assert data["grand_total"] == 48.73


def test_tc04_expired_promo_code():
    """Expired promo code should be rejected; cart total unchanged."""
    response = requests.post(
        f"{BASE_URL}/cart/calculate",
        json={
            "items": [{"sku": "SKU-A", "price": 29.99, "quantity": 1}],
            "promo_code": "FLASH10",  # expired
            "shipping_zip": "90210",
        },
        timeout=10,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["discount"] == 0
    assert data["grand_total"] == 29.99 + data["tax"] + data["shipping"]
