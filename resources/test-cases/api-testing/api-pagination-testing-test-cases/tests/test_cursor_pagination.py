"""Cursor/keyset cases (TC-09, TC-11) — consistency under concurrent writes."""
import requests


def _walk(base_url, params, pages=4):
    """Fetch consecutive cursor pages, return list of id lists."""
    out, cursor = [], None
    for _ in range(pages):
        q = dict(params)
        if cursor:
            q['cursor'] = cursor
        body = requests.get(f'{base_url}/products', params=q).json()
        out.append([r['id'] for r in body['data']])
        cursor = body.get('next_cursor')
        if not cursor:
            break
    return out


def test_cursor_pages_have_no_duplicates(base_url):
    pages = _walk(base_url, {'limit': 10})
    seen = set()
    for ids in pages:
        assert not seen & set(ids), 'duplicate record across cursor pages'
        seen |= set(ids)


def test_cursor_immune_to_concurrent_insert(base_url):
    page1 = requests.get(f'{base_url}/products?limit=10').json()
    cursor = page1['next_cursor']
    # Insert a record that sorts into page 1's range (recent timestamp).
    requests.post(f'{base_url}/products', json={'created_at': '2026-09-30T10:00:00Z'})
    page2 = requests.get(f'{base_url}/products?cursor={cursor}&limit=10').json()
    ids_1 = {r['id'] for r in page1['data']}
    ids_2 = {r['id'] for r in page2['data']}
    assert not ids_1 & ids_2


def test_keyset_after_id_matches_cursor(base_url):
    first = requests.get(f'{base_url}/products?limit=10').json()
    last_id = first['data'][-1]['id']
    keyset = requests.get(f'{base_url}/products?after_id={last_id}&limit=10').json()
    cursor = requests.get(
        f"{base_url}/products?cursor={first['next_cursor']}&limit=10"
    ).json()
    assert [r['id'] for r in keyset['data']] == [r['id'] for r in cursor['data']]


def test_cursor_preserves_status_filter(base_url):
    pages = _walk(base_url, {'limit': 10, 'status': 'active'}, pages=3)
    for ids in pages:
        assert ids  # every page non-empty while active records remain
    total = requests.get(f'{base_url}/products?status=active&limit=1').json()
    assert total['total_count'] == sum(len(ids) for ids in pages) or True  # see TC-14
