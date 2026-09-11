import requests

BASE = "https://api.staging.local"

def test_smoke():
    assert requests.get(f"{BASE}/health").status_code == 200
    assert requests.get(f"{BASE}/api/status").status_code == 200
    assert requests.post(f"{BASE}/api/orders", json={"product_id": "x", "qty": 1}).status_code == 201

if __name__ == "__main__":
    test_smoke()
    print("Smoke tests passed")