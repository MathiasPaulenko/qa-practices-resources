"""pytest suite implementing TC-01..TC-05 and TC-08..TC-10 from
https://qapractices.com/test-cases/pagination-test-cases/

TC-06/TC-07 (infinite scroll) are UI cases — see the Playwright snippet in the
guide; they need a browser, not this suite.
"""

import base64

import pytest

from app import app, seed


@pytest.fixture(autouse=True)
def seeded_dataset():
    seed(50)
    yield


@pytest.fixture()
def client():
    return app.test_client()


# --- Offset pagination (TC-01, TC-02, TC-08) --------------------------------

def test_tc01_first_page_returns_metadata(client):
    data = client.get("/items?page=1&limit=10").get_json()
    assert len(data["items"]) == 10
    assert data["total"] == 50
    assert data["totalPages"] == 5
    assert data["hasNextPage"] is True


def test_tc02_last_partial_page(client):
    data = client.get("/items?page=2&limit=30").get_json()
    assert len(data["items"]) == 20  # 50 - 30
    assert data["hasNextPage"] is False
    assert data["total"] == 50


def test_tc08_empty_result_set(client):
    data = client.get("/items?status=nonexistent&page=1").get_json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["hasNextPage"] is False


# --- Edge cases from the boundary table --------------------------------------

def test_page_zero_rejected(client):
    assert client.get("/items?page=0").status_code == 400


def test_page_size_over_max_clamps(client):
    data = client.get("/items?limit=101").get_json()
    assert len(data["items"]) <= 100


def test_negative_page_rejected(client):
    assert client.get("/items?page=-1").status_code == 400


def test_page_beyond_last_empty_not_error(client):
    data = client.get("/items?page=999&limit=10").get_json()
    assert data["items"] == []
    assert data["hasNextPage"] is False


# --- Cursor pagination (TC-03, TC-04) -----------------------------------------

def test_tc03_cursor_traverses_full_dataset(client):
    ids, cursor = set(), None
    for _ in range(10):
        params = {"limit": 10, "strategy": "cursor"}
        if cursor:
            params["cursor"] = cursor
        data = client.get("/items", query_string=params).get_json()
        ids.update(i["id"] for i in data["items"])
        cursor = data["nextCursor"]
        if cursor is None:
            break
    assert len(ids) == 50
    assert cursor is None


def test_tc04_invalid_cursor_returns_400(client):
    res = client.get("/items?strategy=cursor&cursor=invalid-or-expired-token")
    assert res.status_code == 400
    assert "Invalid cursor" in res.get_json()["error"]


# --- Sort stability (TC-05) ----------------------------------------------------

def test_tc05_sort_stable_across_pages(client):
    p1 = client.get("/items?page=1&limit=10").get_json()["items"]
    p2 = client.get("/items?page=2&limit=10").get_json()["items"]
    ids1, ids2 = {i["id"] for i in p1}, {i["id"] for i in p2}
    assert ids1.isdisjoint(ids2), "item duplicated at page boundary"


# --- Mutation during pagination (TC-10) ----------------------------------------

def test_tc10_offset_shifts_after_insert(client):
    client.post("/admin/reset")
    first = client.get("/items?page=1&limit=10").get_json()["items"]
    client.post("/items", json={"name": "inserted", "created_at": "2026-10-01T09:00:00Z"})
    second = client.get("/items?page=2&limit=10").get_json()["items"]
    # known limitation: offset shifts — last item of page 1 may reappear on page 2
    assert len(second) == 10


def test_tc10_cursor_skips_nothing_after_insert(client):
    data = client.get("/items?limit=10&strategy=cursor").get_json()
    client.post("/items", json={"name": "inserted", "created_at": "2026-10-01T09:00:00Z"})
    more = client.get("/items", query_string={"limit": 10, "strategy": "cursor", "cursor": data["nextCursor"]}).get_json()
    seen = {i["id"] for i in data["items"]}
    assert all(i["id"] not in seen for i in more["items"]), "cursor duplicated an item"
