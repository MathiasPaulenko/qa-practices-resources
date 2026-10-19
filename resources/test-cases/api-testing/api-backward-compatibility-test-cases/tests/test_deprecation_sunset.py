"""Deprecation lifecycle: TC-016 (sunset enforcement), Sunset/Link headers."""
import requests

from conftest import HEADERS


def get(server, path, version=None):
    h = dict(HEADERS)
    if version:
        h["API-Version"] = version
    return requests.get(f"{server}/v1{path}", headers=h)


def test_retired_version_returns_410_gone(server):
    """TC-016: after the sunset date the version dies with 410 + Link header."""
    r = get(server, "/tasks/T-301", "2024-03")
    assert r.status_code == 410
    assert "successor-version" in r.headers.get("Link", "")
    assert "retired" in r.json()["error"]["message"]


def test_stable_version_announces_its_sunset(server):
    """2025-01 advertises a Sunset header while it still serves."""
    r = get(server, "/tasks/T-301", "2025-01")
    assert r.status_code == 200
    assert "Sunset" in r.headers


def test_retired_post_also_returns_410(server):
    """Write paths are retired too — not just reads."""
    r = requests.post(
        f"{server}/v1/tasks",
        headers={**HEADERS, "API-Version": "2024-03"},
        json={"title": "x"},
    )
    assert r.status_code == 410
