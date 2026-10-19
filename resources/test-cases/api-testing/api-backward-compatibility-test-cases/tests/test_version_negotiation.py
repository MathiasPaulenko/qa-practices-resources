"""Version negotiation cases: TC-001, TC-002, TC-003, TC-004, edge cases."""
import requests

from conftest import HEADERS


def get(server, path, version=None):
    h = dict(HEADERS)
    if version:
        h["API-Version"] = version
    return requests.get(f"{server}/v1{path}", headers=h)


def test_old_version_returns_assignee_id(server):
    """TC-001: 2025-01 contract keeps the flat assignee_id field."""
    r = get(server, "/tasks/T-301", "2025-01")
    assert r.status_code == 200
    assert r.json()["assignee_id"] == "U-42"
    assert "assignee" not in r.json()


def test_new_version_returns_assignee_object(server):
    """TC-002: 2026-07 contract returns the nested assignee object."""
    r = get(server, "/tasks/T-301", "2026-07")
    assert r.status_code == 200
    assert r.json()["assignee"]["id"] == "U-42"


def test_missing_version_header_defaults_to_stable(server):
    """TC-003 + edge: no API-Version header falls back to 2025-01."""
    r = get(server, "/tasks/T-301")
    assert r.status_code == 200
    assert r.json()["assignee_id"] == "U-42"


def test_unknown_version_returns_400_with_supported_list(server):
    """TC-004 + edge: unsupported versions are rejected, never silently served."""
    r = get(server, "/tasks/T-301", "2030-01")
    assert r.status_code == 400
    assert "2025-01" in str(r.json())
