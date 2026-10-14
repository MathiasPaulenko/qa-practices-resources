# Data Table Sort & Filter Testing — Companion

Companion resource for [Data Table Sort Filter Test Cases: Column Sort, Search](https://qapractices.com/test-cases/data-table-sort-filter-test-cases/).

## Contents

- `mock_server.py` — stdlib-only mock of the fictional `api.datagridpro.io` orders API used in the article. Implements `GET /v1/orders` with `sort`, `direction`, `page`, `pageSize`, `status`, `from`, `to` and `search` query params, plus Bearer auth.
- `tests/conftest.py` — spins the mock up on an ephemeral port per test.
- `tests/test_orders_api.py` — executable subset of the article's cases: numeric vs lexicographic sort (TC003), search and combined AND filters (TC005/TC008), pagination math and page-count recompute after filtering (TC009/TC016), empty-state payload, special characters, invalid sort field and auth rejection.

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
cd resources/test-cases/ui-component-testing/data-table-sort-filter-test-cases
pytest tests/ -v
```

Run the mock standalone for manual checks:

```bash
python mock_server.py

curl "http://127.0.0.1:8080/v1/orders?sort=amount&direction=asc&pageSize=5" \
  -H "Authorization: Bearer any-token"
```

## What this covers

- Sorting by `amount`, `orderDate`, `customerName` and `status`, ascending and descending, with numeric-aware ordering (2.50 before 10.00).
- Filters: `status`, date range (`from`/`to`, inclusive) and global `search` across id, customer name and status, combined with AND logic.
- Pagination metadata (`page`, `pageSize`, `totalItems`, `totalPages`) and how `totalPages` recomputes when a filter shrinks the result set.
- Error paths: missing Bearer token → `401`, unknown sort field → `400`, special characters in search → safe `200`.
