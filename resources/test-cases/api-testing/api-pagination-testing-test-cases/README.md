# API Pagination Testing — Companion

Companion resource for [API Pagination Testing: 14 Scenarios](https://qapractices.com/test-cases/api-pagination-testing-test-cases).

## Contents

- `mock_server.py` — stdlib-only paginated API (offset, cursor and keyset) over 247 in-memory products, plus `POST /products` for concurrent-insert scenarios
- `tests/conftest.py` — spins the mock server up on an ephemeral port per test session
- `tests/test_boundaries.py` — page-size limits, last page, empty dataset, invalid cursor (edge table + TC-01..07, TC-12)
- `tests/test_cursor_pagination.py` — cursor/keyset consistency, concurrent insert immunity, filter preservation (TC-09, TC-11)
- `tests/test_offset_pagination.py` — full-dataset walk, sort tiebreaker, deep offset, scoped `total_count`, documented offset gap (TC-08, TC-10, TC-13, TC-14)
- `requirements.txt` — pytest 8.3 + requests

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
pytest tests/ -v
```

The mock server can also run standalone for manual checks:

```bash
python mock_server.py 8571
curl "http://127.0.0.1:8571/products?limit=10"
```

The point of the demo: pagination bugs only appear under boundary and concurrency conditions that a happy-path test never touches — deep offsets, partial last pages, mid-pagination inserts, non-unique sort columns. The mock encodes those conditions (shared timestamps, 247 items so `limit=10` produces a partial last page) so every scenario from the guide is reproducible locally.

See the guide for the full test-case tables, the offset-vs-cursor trade-offs and the field story behind TC-10.
