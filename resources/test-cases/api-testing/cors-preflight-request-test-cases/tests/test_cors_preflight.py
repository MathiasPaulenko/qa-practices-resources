"""Maps to the TC-xxx cases in qapractices.com/test-cases/cors-preflight-request-test-cases."""

import pytest

from cors_preflight import (
    CorsConfig,
    credentials_wildcard_violation,
    evaluate_preflight,
    is_simple_request,
    origin_matches,
)

API = CorsConfig(
    allowed_origins=["https://checkout.apigateway.io", "https://admin.apigateway.io"],
    allowed_methods=["GET", "POST", "PUT", "DELETE"],
    allowed_headers=["content-type", "x-api-key", "x-idempotency-key", "authorization"],
    allow_credentials=True,
    max_age=86400,
)
CHECKOUT = "https://checkout.apigateway.io"


def test_tc001_simple_get_needs_no_preflight():
    assert is_simple_request("GET", {"Accept": "application/json"})


def test_tc002_json_post_triggers_preflight():
    assert not is_simple_request("POST", {"Content-Type": "application/json"})


def test_tc003_custom_header_triggers_preflight():
    assert not is_simple_request("GET", {"X-Api-Key": "k_live_abc123"})


def test_tc004_each_allowed_origin_gets_its_echo():
    for origin in API.allowed_origins:
        result = evaluate_preflight(API, origin, "GET", [])
        assert result["allowed"], origin


def test_tc005_credentials_with_specific_origin_allowed():
    result = evaluate_preflight(API, CHECKOUT, "GET", [], with_credentials=True)
    assert result["allowed"]


def test_tc011_disallowed_origin_blocked():
    result = evaluate_preflight(API, "https://evil-site.example", "GET", [])
    assert not result["allowed"]
    assert "not in allow-list" in result["reason"]


def test_tc012_disallowed_method_blocked():
    result = evaluate_preflight(API, CHECKOUT, "PATCH", [])
    assert not result["allowed"]
    assert "PATCH" in result["reason"]


def test_tc013_disallowed_header_blocked():
    result = evaluate_preflight(API, CHECKOUT, "GET", ["X-Forbidden-Header"])
    assert not result["allowed"]
    assert "x-forbidden-header" in result["reason"]


def test_tc014_wildcard_with_credentials_is_violation():
    assert credentials_wildcard_violation("*", allow_credentials=True)
    config = CorsConfig(
        allow_any_origin=True,
        allowed_methods=["GET", "POST"],
        allowed_headers=["content-type"],
        allow_credentials=True,
    )
    result = evaluate_preflight(config, "https://anything.example", "GET", [], with_credentials=True)
    assert not result["allowed"]
    assert "wildcard" in result["reason"]


def test_tc017_credentials_without_allow_credentials_blocked():
    config = CorsConfig(
        allowed_origins=[CHECKOUT],
        allowed_methods=["GET"],
        allowed_headers=["content-type"],
        allow_credentials=False,
    )
    result = evaluate_preflight(config, CHECKOUT, "GET", [], with_credentials=True)
    assert not result["allowed"]


def test_tc019_multiple_custom_headers_evaluated_together():
    result = evaluate_preflight(API, CHECKOUT, "GET", ["X-Api-Key", "X-Client-Id"])
    assert not result["allowed"]  # X-Client-Id is not in the allow-list
    result2 = evaluate_preflight(API, CHECKOUT, "GET", ["X-Api-Key", "Authorization"])
    assert result2["allowed"]


def test_tc021_null_origin_rejected():
    result = evaluate_preflight(API, "null", "GET", [])
    assert not result["allowed"]


@pytest.mark.parametrize(
    "origin,allowed,expected",
    [
        ("https://sub.checkout.apigateway.io", "https://checkout.apigateway.io", False),  # TC022
        ("http://checkout.apigateway.io", "https://checkout.apigateway.io", False),        # TC024
        ("https://checkout.apigateway.io:8080", "https://checkout.apigateway.io", False),  # TC025
        ("https://checkout.apigateway.io", "https://checkout.apigateway.io", True),
    ],
)
def test_origin_tuple_match(origin, allowed, expected):
    assert origin_matches(origin, allowed) is expected


def test_tc029_authorization_header_allowed():
    result = evaluate_preflight(API, CHECKOUT, "GET", ["Authorization"])
    assert result["allowed"]
    assert result["cache_seconds"] == 86400


def test_max_age_zero_means_no_cache():
    config = CorsConfig(allowed_origins=[CHECKOUT], allowed_methods=["GET"], allowed_headers=[], max_age=0)
    assert evaluate_preflight(config, CHECKOUT, "GET", [])["cache_seconds"] == 0
