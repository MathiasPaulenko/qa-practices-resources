"""Executable subset of the data table sort/filter test cases on qapractices.com.

Covers the API-level assertions behind TC003 (numeric sort), TC005/TC008
(search and combined filters), TC009/TC016 (pagination math) and the
edge cases around empty results and auth.
"""

import requests

AUTH = {"Authorization": "Bearer test-token"}


def get(server, query=""):
    url = "%s/v1/orders%s" % (server, ("?" + query) if query else "")
    return requests.get(url, headers=AUTH, timeout=5)


def test_requires_auth(server):
    r = requests.get("%s/v1/orders" % server, timeout=5)
    assert r.status_code == 401


def test_amount_sort_is_numeric_not_lexicographic(server):
    r = get(server, "sort=amount&direction=asc&pageSize=60")
    amounts = [o["amount"] for o in r.json()["orders"]]
    assert amounts == sorted(amounts)
    # String sort would place 10.00 before 2.50 — assert real numeric order.
    assert amounts[0] == min(amounts)


def test_amount_sort_descending(server):
    r = get(server, "sort=amount&direction=desc&pageSize=60")
    amounts = [o["amount"] for o in r.json()["orders"]]
    assert amounts == sorted(amounts, reverse=True)


def test_status_filter_returns_only_matching_rows(server):
    r = get(server, "status=shipped&pageSize=60")
    body = r.json()
    assert body["totalItems"] > 0
    assert all(o["status"] == "shipped" for o in body["orders"])
    assert body["filters"]["status"] == "shipped"


def test_date_range_filter_is_inclusive(server):
    r = get(server, "from=2026-07-01&to=2026-07-10&pageSize=60")
    dates = [o["orderDate"] for o in r.json()["orders"]]
    assert dates
    assert all("2026-07-01" <= d <= "2026-07-10" for d in dates)


def test_global_search_matches_any_column(server):
    r = get(server, "search=Acme&pageSize=60")
    body = r.json()
    assert body["totalItems"] > 0
    assert all("acme" in o["customerName"].lower() for o in body["orders"])
    assert body["search"] == "Acme"


def test_combined_filters_apply_and_logic(server):
    r = get(server, "status=delivered&search=Acme&pageSize=60")
    for o in r.json()["orders"]:
        assert o["status"] == "delivered"
        assert "acme" in o["customerName"].lower()


def test_pagination_pages_are_disjoint(server):
    p1 = get(server, "page=1&pageSize=10").json()
    p2 = get(server, "page=2&pageSize=10").json()
    assert p1["totalItems"] == 60 and p1["totalPages"] == 6
    ids1 = {o["id"] for o in p1["orders"]}
    ids2 = {o["id"] for o in p2["orders"]}
    assert ids1.isdisjoint(ids2)
    assert len(p1["orders"]) == len(p2["orders"]) == 10


def test_filter_recomputes_total_pages(server):
    unfiltered = get(server, "pageSize=10").json()
    filtered = get(server, "status=shipped&pageSize=10").json()
    assert filtered["totalItems"] < unfiltered["totalItems"]
    expected_pages = -(-filtered["totalItems"] // 10)
    assert filtered["totalPages"] == expected_pages


def test_search_with_no_results_returns_empty_state_payload(server):
    r = get(server, "search=xyznonexistent")
    body = r.json()
    assert r.status_code == 200
    assert body["orders"] == [] and body["totalItems"] == 0


def test_search_special_characters_do_not_crash(server):
    r = get(server, "search=%21%40%23%24%25%5E%26*()")
    assert r.status_code == 200


def test_invalid_sort_field_returns_400(server):
    r = get(server, "sort=bogus")
    assert r.status_code == 400
    assert r.json()["error"] == "invalid_sort_field"


def test_sort_metadata_echoes_field_and_direction(server):
    body = get(server, "sort=orderDate&direction=desc").json()
    assert body["sort"] == {"field": "orderDate", "direction": "desc"}
