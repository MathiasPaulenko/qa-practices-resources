# tests/test_inventory.py
# Requires: Python 3.12, pytest 8.3, requests 2.32
"""Test inventory limits and overselling prevention."""
import pytest
import requests

BASE_URL = "https://staging.qa.local/api"


def test_tc08_prevent_overselling():
    """TC-08: Adding more than available stock should cap at max."""
    response = requests.post(
        f"{BASE_URL}/cart/items",
        json={"sku": "SKU-LIMITED", "quantity": 4},  # stock is 3
        timeout=10,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 3
    assert "Only 3 units available" in data["message"]


def test_tc08_exact_stock_checkout():
    """Adding exact stock quantity should allow checkout."""
    response = requests.post(
        f"{BASE_URL}/cart/items",
        json={"sku": "SKU-LIMITED", "quantity": 3},
        timeout=10,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 3
    assert data["checkout_enabled"] is True


def test_tc08_zero_stock_blocks_add():
    """Zero-stock item should not be added to cart."""
    response = requests.post(
        f"{BASE_URL}/cart/items",
        json={"sku": "SKU-OUTOFSTOCK", "quantity": 1},
        timeout=10,
    )
    assert response.status_code == 409
    data = response.json()
    assert "Out of stock" in data["error"]
