# Infinite Scroll Pagination Test Cases — Companion Lab

Companion for [Infinite Scroll Pagination Test Cases: TaskFlow Example](https://qapractices.com/test-cases/infinite-scroll-pagination-test-cases/) on QAPractices.

Pure-stdlib Python model of an infinite-scroll feed: `PaginatedAPI` serves
offset pages (`page=N`, `hasMore`, injectable failures) and `ScrollFeed` plays
the client — threshold fetch, append with id dedupe, end-of-feed detection and
idempotent retry.

## Layout

```text
paginated_feed.py              — PaginatedAPI + ScrollFeed + make_tasks helper
tests/test_paginated_feed.py   — pytest cases mapped to TC-xxx on the site
requirements.txt               — pytest 8.3.4
pytest.ini                     — testpaths/pythonpath
```

## Run

```bash
pip install -r requirements.txt
pytest -q
```

## Coverage

First/partial/last pages, page-2 append with dedupe by id, end-of-feed
termination (no `page=6` request), mid-scroll errors preserving rendered
items, idempotent retry, duplicated page rejection, empty feed, and the
boundary cases (exact multiple vs total+1).

The model is offline and deterministic — use it to prototype dedupe/retry
logic before wiring the real `IntersectionObserver` implementation.
