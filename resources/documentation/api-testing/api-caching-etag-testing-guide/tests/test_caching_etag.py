import requests

BASE = "https://api.staging.local"


def test_first_get_returns_etag_and_cache_control():
    first = requests.get(f"{BASE}/products/123")
    assert first.status_code == 200
    assert "ETag" in first.headers
    assert "Cache-Control" in first.headers


def test_conditional_get_with_matching_etag_returns_304():
    first = requests.get(f"{BASE}/products/123")
    etag = first.headers["ETag"]

    second = requests.get(f"{BASE}/products/123", headers={"If-None-Match": etag})
    assert second.status_code == 304
    assert second.content == b""


def test_mutation_changes_etag():
    first = requests.get(f"{BASE}/products/123")
    etag = first.headers["ETag"]

    requests.put(f"{BASE}/products/123", json={"price": 19.99})
    updated = requests.get(f"{BASE}/products/123", headers={"If-None-Match": etag})
    assert updated.status_code == 200
    assert updated.headers["ETag"] != etag