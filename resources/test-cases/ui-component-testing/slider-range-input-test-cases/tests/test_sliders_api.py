"""Executable subset of the slider-range-input test cases.

Covers the API-side assertions behind the article's curl examples:
price-range filtering, step/min/max validation, dual-handle gap
enforcement and preference persistence.
"""

import pytest
import requests

AUTH = {"Authorization": "Bearer test-token"}
PRICES = {"min": 0, "max": 1000, "step": 5}


# --- GET /v1/products -------------------------------------------------------

def test_products_filter_by_price_range(api):
    r = requests.get(
        api + "/v1/products",
        params={"minPrice": 50, "maxPrice": 500, "step": 5,
                "page": 1, "pageSize": 20},
        headers=AUTH, timeout=5,
    )
    assert r.status_code == 200
    data = r.json()
    assert data["filter"] == {"minPrice": 50.0, "maxPrice": 500.0, "step": 5.0}
    assert all(50 <= p["price"] <= 500 for p in data["products"])
    assert all(p["price"] % 5 == 0 for p in data["products"])


def test_products_pagination(api):
    r1 = requests.get(api + "/v1/products",
                      params={"page": 1, "pageSize": 10}, headers=AUTH, timeout=5).json()
    r2 = requests.get(api + "/v1/products",
                      params={"page": 2, "pageSize": 10}, headers=AUTH, timeout=5).json()
    assert len(r1["products"]) == 10
    assert r1["products"][0]["id"] != r2["products"][0]["id"]
    assert r1["totalItems"] == 342


def test_products_requires_auth(api):
    r = requests.get(api + "/v1/products", timeout=5)
    assert r.status_code == 401


# --- POST /v1/sliders/validate ----------------------------------------------

def test_validate_accepts_step_multiple(api):
    r = requests.post(api + "/v1/sliders/validate",
                      json=dict(PRICES, value=505), timeout=5)
    assert r.json()["valid"] is True


def test_validate_rejects_non_step_value(api):
    r = requests.post(api + "/v1/sliders/validate",
                      json=dict(PRICES, value=503), timeout=5)
    data = r.json()
    assert data["valid"] is False
    assert data["nearestValidValue"] in (500, 505)
    assert "step" in data["error"]


@pytest.mark.parametrize("value,nearest", [(-50, 0), (1500, 1000)])
def test_validate_clamps_out_of_range(api, value, nearest):
    r = requests.post(api + "/v1/sliders/validate",
                      json=dict(PRICES, value=value), timeout=5)
    data = r.json()
    assert data["valid"] is False
    assert data["nearestValidValue"] == nearest


def test_validate_rejects_non_numeric(api):
    r = requests.post(api + "/v1/sliders/validate",
                      json=dict(PRICES, value="abc"), timeout=5)
    assert r.status_code == 400


# --- POST /v1/sliders/validate-range ----------------------------------------

def test_range_rejects_crossed_handles(api):
    r = requests.post(api + "/v1/sliders/validate-range",
                      json=dict(PRICES, leftHandle=500, rightHandle=50, gap=10),
                      timeout=5)
    data = r.json()
    assert data["valid"] is False
    assert "must be less than" in data["error"]


@pytest.mark.parametrize("left,right,gap,expected", [
    (490, 500, 10, True),    # exactly at the gap boundary: allowed
    (495, 500, 10, False),   # inside the gap: rejected
    (200, 800, 10, True),    # wide range: allowed
])
def test_range_min_gap_boundary(api, left, right, gap, expected):
    r = requests.post(api + "/v1/sliders/validate-range",
                      json=dict(PRICES, leftHandle=left, rightHandle=right, gap=gap),
                      timeout=5)
    assert r.json()["valid"] is expected


# --- POST /v1/users/{id}/preferences -----------------------------------------

def test_save_preference(api):
    r = requests.post(
        api + "/v1/users/U-22/preferences",
        json={"filterName": "Mid-cap stocks", "minPrice": 50,
              "maxPrice": 500, "step": 5},
        headers=AUTH, timeout=5,
    )
    data = r.json()
    assert r.status_code == 200
    assert data["preferenceId"].startswith("PREF-")
    assert data["userId"] == "U-22"
    assert data["minPrice"] == 50 and data["maxPrice"] == 500


def test_save_preference_requires_auth(api):
    r = requests.post(api + "/v1/users/U-22/preferences",
                      json={"filterName": "x", "minPrice": 0,
                            "maxPrice": 10, "step": 5},
                      timeout=5)
    assert r.status_code == 401
