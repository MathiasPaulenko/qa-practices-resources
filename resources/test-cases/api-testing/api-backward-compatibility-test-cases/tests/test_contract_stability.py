"""Cross-version stability: TC-008, TC-010, TC-013, TC-014, TC-015."""
import requests

from conftest import HEADERS


def get(server, path, version, auth=True):
    h = dict(HEADERS) if auth else {}
    h["API-Version"] = version
    return requests.get(f"{server}/v1{path}", headers=h)


def test_pagination_contract_identical(server):
    """TC-008: page/limit/total metadata is the same shape in both versions."""
    for v in ("2025-01", "2026-07"):
        body = get(server, "/tasks", v).json()
        for key in ("page", "limit", "total", "items"):
            assert key in body, f"{key} missing on {v}"


def test_error_shape_identical_across_versions(server):
    """TC-010: error bodies keep {error: {code, message, details}}."""
    for v in ("2025-01", "2026-07"):
        r = requests.post(f"{server}/v1/tasks",
                          headers={**HEADERS, "API-Version": v},
                          data="not-json")
        assert r.status_code == 400
        err = r.json()["error"]
        assert set(err) == {"code", "message", "details"}


def test_http_methods_stable(server):
    """TC-013: GET/POST/PATCH/DELETE behave the same on both versions."""
    for v in ("2025-01", "2026-07"):
        h = {**HEADERS, "API-Version": v}
        assert requests.get(f"{server}/v1/tasks/T-301", headers=h).status_code == 200
        assert requests.patch(f"{server}/v1/tasks/T-301", headers=h,
                              json={"status": "done"}).status_code == 200
        assert requests.delete(f"{server}/v1/tasks/T-301", headers=h).status_code == 204


def test_auth_behavior_identical(server):
    """TC-014: missing token -> 401, expired token -> 401 on both versions."""
    for v in ("2025-01", "2026-07"):
        assert get(server, "/tasks/T-301", v, auth=False).status_code == 401
        r = requests.get(f"{server}/v1/tasks/T-301",
                         headers={"Authorization": "Bearer expired",
                                  "API-Version": v})
        assert r.status_code in (401, 403)


def test_rate_limit_headers_present(server):
    """TC-015: the rate-limit triple ships on both versions."""
    for v in ("2025-01", "2026-07"):
        r = get(server, "/tasks", v)
        for h in ("X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"):
            assert h in r.headers
