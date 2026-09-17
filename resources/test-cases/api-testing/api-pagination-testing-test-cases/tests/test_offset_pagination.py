"""Offset cases (TC-08, TC-10, TC-13, TC-14)."""
import time

import requests


def test_offset_pages_cover_full_dataset(base_url):
    seen = set()
    page = 1
    while True:
        body = requests.get(f'{base_url}/products?page={page}&limit=50').json()
        seen |= {r['id'] for r in body['data']}
        if not body['has_next_page']:
            break
        page += 1
    assert len(seen) == 247


def test_sort_stability_with_tiebreaker(base_url):
    """TC-10: rows sharing a created_at still get a deterministic order via id."""
    timestamps = []
    page = 1
    while page <= 5:
        body = requests.get(f'{base_url}/products?page={page}&limit=50').json()
        timestamps += [(r['created_at'], r['id']) for r in body['data']]
        if not body['has_next_page']:
            break
        page += 1
    assert timestamps == sorted(timestamps, key=lambda t: (t[0], t[1]), reverse=True)


def test_deep_offset_still_fast(base_url):
    start = time.perf_counter()
    r = requests.get(f'{base_url}/products?offset=240&limit=10')
    assert r.status_code == 200
    assert time.perf_counter() - start < 0.5


def test_total_count_scoped_to_filter(base_url):
    active = requests.get(f'{base_url}/products?status=active&limit=10').json()
    archived = requests.get(f'{base_url}/products?status=archived&limit=10').json()
    assert active['total_count'] + archived['total_count'] == 247
    assert active['total_count'] != 247  # not the unfiltered table size


def test_offset_concurrent_insert_behavior_documented(base_url):
    """TC-08: records what offset does under a mid-pagination insert.

    Offset is NOT immune — this test documents (not asserts) the gap:
    after an insert that sorts before page 1, page 2 may repeat or skip.
    """
    p1 = requests.get(f'{base_url}/products?page=1&limit=10').json()
    requests.post(f'{base_url}/products', json={'created_at': '2026-09-30T10:00:00Z'})
    p2 = requests.get(f'{base_url}/products?page=2&limit=10').json()
    overlap = {r['id'] for r in p1['data']} & {r['id'] for r in p2['data']}
    # With offset semantics the last row of the old page 1 shifts into page 2.
    # A duplicate here is expected behavior — assert it surfaces predictably.
    assert len(overlap) <= 1
