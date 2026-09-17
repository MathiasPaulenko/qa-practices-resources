"""Boundary and input-validation cases (edge table + TC-01..TC-07, TC-12)."""
import requests


def test_default_page_size(base_url):
    r = requests.get(f'{base_url}/products').json()
    assert len(r['data']) == 20
    assert r['total_count'] == 247


def test_explicit_limit_in_range(base_url):
    r = requests.get(f'{base_url}/products?limit=50').json()
    assert len(r['data']) == 50
    assert r['limit'] == 50


def test_limit_at_maximum(base_url):
    r = requests.get(f'{base_url}/products?limit=100').json()
    assert len(r['data']) == 100


def test_limit_above_maximum_rejected(base_url):
    r = requests.get(f'{base_url}/products?limit=500')
    assert r.status_code == 400


def test_limit_zero_or_negative_rejected(base_url):
    for bad in ('0', '-1', 'abc'):
        assert requests.get(f'{base_url}/products?limit={bad}').status_code == 400


def test_last_page_partial_results(base_url):
    r = requests.get(f'{base_url}/products?page=25&limit=10').json()
    assert len(r['data']) == 7
    assert r['has_next_page'] is False
    assert r['total_count'] == 247


def test_page_beyond_last(base_url):
    r = requests.get(f'{base_url}/products?page=999&limit=10')
    assert r.status_code == 200
    assert r.json()['data'] == []


def test_empty_dataset_via_filter(base_url):
    r = requests.get(f'{base_url}/products?status=nonexistent&limit=10').json()
    assert r['data'] == []
    assert r['total_count'] == 0
    assert r['has_next_page'] is False


def test_minimum_limit(base_url):
    r = requests.get(f'{base_url}/products?limit=1').json()
    assert len(r['data']) == 1
    assert r['has_next_page'] is True


def test_invalid_cursor_rejected(base_url):
    r = requests.get(f'{base_url}/products?cursor=abc123bogus')
    assert r.status_code == 400
    assert 'Invalid or expired cursor' in r.json()['error']
