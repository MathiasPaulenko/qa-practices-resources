"""Error-handling contract checks for an HTTP API.

Companion to https://qapractices.com/test-cases/api-error-handling-test-cases/
Covers TC-001, TC-002, TC-006, TC-009 and TC-017 from that suite.

Set API_BASE_URL before running:

    export API_BASE_URL="https://api.staging.example.com/api/v1"
    pytest test_error_handling.py -v
"""

import json
import os
from pathlib import Path

import pytest
import requests

BASE_URL = os.environ.get("API_BASE_URL")
SCHEMA = json.loads(
    (Path(__file__).parent / "problem-details-schema.json").read_text(encoding="utf-8")
)

pytestmark = pytest.mark.skipif(
    not BASE_URL, reason="set API_BASE_URL to run the error-contract checks"
)


def assert_problem_details(res: requests.Response, expected_status: int) -> dict:
    """Every error body must follow the RFC 9457 problem-details contract."""
    assert res.status_code == expected_status, res.text[:300]
    assert res.headers["Content-Type"].startswith("application/problem+json"), (
        res.headers.get("Content-Type")
    )
    body = res.json()
    import jsonschema

    jsonschema.validate(body, SCHEMA)
    assert body["status"] == expected_status
    return body


def test_unknown_route_returns_structured_404():  # TC-001
    res = requests.get(f"{BASE_URL}/definitely-not-a-route", timeout=10)
    body = assert_problem_details(res, 404)
    assert body["title"]
    assert "stack" not in json.dumps(body).lower()  # no internals leaked


def test_wrong_method_lists_allowed_verbs():  # TC-002
    res = requests.delete(f"{BASE_URL}/users/42", timeout=10)
    assert_problem_details(res, 405)
    assert "GET" in res.headers["Allow"]


def test_missing_auth_returns_challenge():  # TC-006
    res = requests.get(f"{BASE_URL}/users/42", timeout=10)
    body = assert_problem_details(res, 401)
    assert "WWW-Authenticate" in res.headers
    assert res.headers["WWW-Authenticate"].startswith("Bearer")
    assert body["detail"]  # human-readable, but no resource data


def test_over_quota_returns_retryable_429():  # TC-009
    quota = int(os.environ.get("API_RATE_LIMIT", "100"))
    for _ in range(quota + 1):
        res = requests.get(f"{BASE_URL}/search", params={"q": "test"}, timeout=10)
        if res.status_code == 429:
            break
    assert res.status_code == 429, "quota never tripped — set API_RATE_LIMIT"
    assert int(res.headers["Retry-After"]) > 0
    assert_problem_details(res, 429)


def test_every_error_shares_the_contract():  # TC-017
    failures = [
        requests.get(f"{BASE_URL}/definitely-not-a-route", timeout=10),
        requests.delete(f"{BASE_URL}/users/42", timeout=10),
        requests.get(f"{BASE_URL}/users/42", timeout=10),
    ]
    shapes = set()
    for res in failures:
        body = assert_problem_details(res, res.status_code)
        shapes.add(tuple(sorted(body.keys())))
    assert len(shapes) == 1, f"inconsistent error shapes: {shapes}"
