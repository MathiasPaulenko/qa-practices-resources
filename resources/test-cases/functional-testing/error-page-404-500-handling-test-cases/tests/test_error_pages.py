"""Pytest suite for the error-page mock server.

Maps the article's test cases to HTTP-level assertions: status codes,
headers, content negotiation, redirect chains, soft 404s, stack-trace
leaks and rate limiting — the checks you can run without a browser.
"""

import pytest
import requests

MISSING_URL = "/product/legacy-summer-sneakers-2024"


def test_404_returns_real_status_not_soft_404(session, base_url):
    """TC002/TC016 — a missing page must return 404, never 200."""
    resp = session.get(f"{base_url}{MISSING_URL}")
    assert resp.status_code == 404
    assert "text/html" in resp.headers["Content-Type"]


def test_soft_404_endpoint_is_detectable(session, base_url):
    """TC016 — the misconfigured route returns 200 with 404 content.

    This is exactly the defect TC016 hunts: the assertion below proves
    the bug exists on this route, which is what a real 404 check would
    catch in production.
    """
    resp = session.get(f"{base_url}/misconfigured/404")
    assert resp.status_code == 200  # the bug: should be 404
    assert "Page Not Found" in resp.text  # 404 content under a 200


def test_404_page_has_navigation_search_and_noindex(session, base_url):
    """TC001/TC007 — custom 404 with nav, search, suggestions, noindex."""
    resp = session.get(f"{base_url}{MISSING_URL}")
    body = resp.text
    assert "Page Not Found" in body
    assert 'name="robots" content="noindex"' in body
    assert '<a href="/">' in body  # home link
    assert 'type="search"' in body  # search bar
    assert "suggestions" in body


def test_api_404_returns_json_for_json_clients(session, base_url):
    """TC026 — Accept: application/json must get a JSON 404 body."""
    resp = session.get(
        f"{base_url}/api/v1/products/99999",
        headers={"Accept": "application/json"},
    )
    assert resp.status_code == 404
    assert resp.headers["Content-Type"] == "application/json"
    assert resp.json() == {
        "error": "Not Found",
        "message": "Product 99999 not found",
        "status": 404,
    }


def test_api_404_negotiation_html_clients_get_html(session, base_url):
    """TC026 — browsers on the same endpoint get the HTML page."""
    resp = session.get(
        f"{base_url}/api/v1/products/99999",
        headers={"Accept": "text/html"},
    )
    assert resp.status_code == 404
    assert "text/html" in resp.headers["Content-Type"]
    assert "Page Not Found" in resp.text


def test_500_page_is_generic_and_not_cached(session, base_url):
    """TC004/TC031 — 500 with no-store, no stack trace in the body."""
    resp = session.get(f"{base_url}/boom")
    assert resp.status_code == 500
    assert resp.headers["Cache-Control"] == "no-store"
    assert "Traceback" not in resp.text
    assert "postgres://" not in resp.text


def test_debug_500_leaks_stack_trace_and_credentials(session, base_url):
    """TC017 — the misconfigured endpoint leaks internals (defect demo)."""
    resp = session.get(f"{base_url}/misconfigured/500-debug")
    assert resp.status_code == 500
    # The leaked details below are exactly what TC017 must catch.
    assert "Traceback" in resp.text
    assert "/srv/urbanthreads" in resp.text
    assert "db.internal" in resp.text


def test_403_forbidden_page(session, base_url):
    """TC010 — unauthenticated access to /admin/reports returns 403."""
    resp = session.get(f"{base_url}/admin/reports")
    assert resp.status_code == 403
    assert 'href="/login"' in resp.text


def test_413_payload_too_large(session, base_url):
    """TC032 — uploads over the 10 MB limit are rejected with 413."""
    resp = session.post(
        f"{base_url}/returns/upload",
        data=b"x" * (15 * 1024 * 1024),  # 15 MB, over the limit
    )
    assert resp.status_code == 413


def test_429_rate_limit_includes_retry_after(session, base_url, rate_limit):
    """TC033 — request N+1 over the limit returns 429 + Retry-After."""
    for _ in range(rate_limit + 1):
        resp = session.get(f"{base_url}/ratelimited")
    assert resp.status_code == 429
    assert "Retry-After" in resp.headers
    assert int(resp.headers["Retry-After"]) > 0


def test_503_maintenance_has_retry_after(session, base_url):
    """TC012 — maintenance mode returns 503 + Retry-After."""
    resp = session.get(f"{base_url}/maintenance")
    assert resp.status_code == 503
    assert resp.headers["Retry-After"] == "3600"


def test_redirect_loop_is_detectable(session, base_url):
    """TC025 — requests raises TooManyRedirects on the loop route."""
    with pytest.raises(requests.TooManyRedirects):
        session.get(f"{base_url}/loop")


def test_redirect_chain_ends_at_real_404(session, base_url):
    """Edge case — a 301 chain must terminate at a real 404, no loop."""
    resp = session.get(f"{base_url}/old-product")
    assert resp.status_code == 404
    assert len(resp.history) == 1
    assert resp.history[0].status_code == 301


def test_sitemap_excludes_error_pages(session, base_url):
    """TC023 — sitemap.xml contains only valid URLs."""
    resp = session.get(f"{base_url}/sitemap.xml")
    assert resp.status_code == 200
    for bad in ("404", "500", "boom", "admin/reports", "misconfigured"):
        assert bad not in resp.text


def test_server_header_does_not_leak_version(session, base_url):
    """TC022 — the Server header carries no version tokens."""
    resp = session.get(f"{base_url}/boom")
    server = resp.headers.get("Server", "")
    assert not any(ch.isdigit() for ch in server)
    assert "nginx" not in server.lower()
    assert "Apache" not in server
