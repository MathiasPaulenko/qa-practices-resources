"""Post-Deploy Smoke Test

Verifies health endpoint and version after deployment.
Usage: python post-deploy-smoke-test.py
Requires: requests 2.31+
"""
import requests

BASE = "https://app.qa.local"


def test_health_and_version():
    health = requests.get(f"{BASE}/health", timeout=10)
    assert health.status_code == 200
    assert health.json()["version"] == "2.4.1"
    assert health.json()["environment"] == "production"


if __name__ == "__main__":
    test_health_and_version()
    print("Post-deploy smoke test passed")
