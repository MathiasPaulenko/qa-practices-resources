"""Field-level compatibility: TC-005, TC-006, TC-007, TC-009, edge cases."""
import requests

from conftest import HEADERS


def get(server, path, version):
    return requests.get(f"{server}/v1{path}",
                        headers={**HEADERS, "API-Version": version})


def test_deprecated_field_dual_shipped(server):
    """TC-005 + edge: 2026-07 keeps assignee_id during transition + Deprecation header."""
    r = get(server, "/tasks/T-301", "2026-07")
    assert r.status_code == 200
    body = r.json()
    assert "assignee" in body and body["assignee_id"] == "U-42"
    assert r.headers.get("Deprecation") == "true"


def test_new_optional_field_absent_on_old_version(server):
    """TC-006: story_points only exists in the 2026-07 contract."""
    old = get(server, "/tasks/T-301", "2025-01").json()
    new = get(server, "/tasks/T-301", "2026-07").json()
    assert "story_points" not in old
    assert "story_points" in new


def test_removed_field_never_null_on_old_version(server):
    """TC-007: 2025-01 returns the real value, not null."""
    old = get(server, "/tasks/T-301", "2025-01").json()
    assert old["assignee_id"] == "U-42"


def test_status_enum_rejected_in_new_version(server):
    """Edge: removed enum value is rejected with allowed values listed."""
    r = requests.patch(
        f"{server}/v1/tasks/T-301",
        headers={**HEADERS, "API-Version": "2026-07"},
        json={"status": "blocked"},
    )
    assert r.status_code in (400, 422)
    assert "done" in str(r.json())


def test_new_required_field_in_new_version(server):
    """Edge: POST without project_id fails on 2026-07."""
    r = requests.post(
        f"{server}/v1/tasks",
        headers={**HEADERS, "API-Version": "2026-07"},
        json={"title": "x"},
    )
    assert r.status_code == 422


def test_old_client_write_mapped_with_deprecation(server):
    """Edge: posting assignee_id on 2026-07 still succeeds, flagged deprecated."""
    r = requests.post(
        f"{server}/v1/tasks",
        headers={**HEADERS, "API-Version": "2026-07"},
        json={"title": "x", "project_id": "P-12", "assignee_id": "U-42"},
    )
    assert r.status_code == 201
    assert r.headers.get("Deprecation") == "true"
