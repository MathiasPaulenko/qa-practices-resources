# Performance Optimization — Companion

Companion files for the [Performance Optimization Guide](https://qapractices.com/documentation/performance-optimization).

## Files

| File | Purpose |
| --- | --- |
| `src/cursor_pagination.py` | Cursor pagination helper: base64-encoded cursor, O(limit) at any depth. |
| `src/n_plus_one.py` | N+1 ORM anti-pattern vs `prefetch_related` (Django, illustrative). |
| `sql/index-optimization.sql` | PostgreSQL index patterns by scenario + EXPLAIN ANALYZE + unused-index query. |
| `redis/cache-invalidation.md` | Redis caching commands: TTL, tag-based invalidation, cache warming notes. |
| `nginx/gzip.conf` | Response compression for JSON APIs (5-10x on JSON). |
| `tests/test_cursor_pagination.py` | Pytest suite for the pagination helper — stdlib only, no database needed. |

## Requirements

- Python 3.10+
- pytest 8.3+
- (optional) Django 5.x for the N+1 example; PostgreSQL for the SQL snippets

## Usage

1. Install dependencies: `pip install -r requirements.txt`.
2. Run `pytest tests/ -v` — verifies cursor encoding, page continuity, and end-of-list behavior.
3. Copy `sql/index-optimization.sql` patterns into your migration tooling; run `EXPLAIN (ANALYZE, BUFFERS)` before and after each index.
4. Apply `nginx/gzip.conf` to the API's nginx config.

## CI Integration

```yaml
- run: pip install -r requirements.txt && pytest tests/ -v --tb=short
```
