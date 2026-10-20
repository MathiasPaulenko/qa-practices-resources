"""Maps to the TC-xxx cases in qapractices.com/test-cases/infinite-scroll-pagination-test-cases."""

import pytest

from paginated_feed import PaginatedAPI, ScrollFeed, make_tasks


def test_tc001_first_page_loads_page_size():
    feed = ScrollFeed(PaginatedAPI(make_tasks(83), page_size=20))
    assert feed.load_next()
    assert len(feed.rendered) == 20
    assert feed.rendered[0].id == "T-001"


def test_tc002_second_scroll_fires_page_2_and_appends():
    feed = ScrollFeed(PaginatedAPI(make_tasks(83), page_size=20))
    feed.load_next()
    feed.load_next()
    assert feed.api.requests == [1, 2]
    assert len(feed.rendered) == 40
    assert feed.rendered[20].id == "T-021"


def test_tc004_end_of_feed_stops_requests():
    feed = ScrollFeed(PaginatedAPI(make_tasks(83), page_size=20))
    for _ in range(5):
        feed.load_next()
    assert feed.ended
    assert len(feed.rendered) == 83
    assert feed.api.requests == [1, 2, 3, 4, 5]
    assert not feed.load_next()  # no page=6 request
    assert feed.api.requests == [1, 2, 3, 4, 5]


def test_tc005_network_error_preserves_rendered_items():
    feed = ScrollFeed(PaginatedAPI(make_tasks(83), page_size=20))
    feed.load_next()
    feed.load_next()
    feed.api.fail_next = 1
    assert not feed.load_next()
    assert feed.last_error is not None
    assert len(feed.rendered) == 40  # pages 1-2 intact


def test_tc006_retry_after_transient_error():
    feed = ScrollFeed(PaginatedAPI(make_tasks(83), page_size=20))
    feed.load_next()
    feed.api.fail_next = 1
    assert not feed.load_next()
    assert feed.retry()
    assert feed.last_error is None
    assert len(feed.rendered) == 40
    assert feed.duplicates_rejected == 0


def test_tc014_duplicate_page_deduped_by_id():
    api = PaginatedAPI(make_tasks(20) + make_tasks(20), page_size=20)  # page 2 repeats page 1
    feed = ScrollFeed(api)
    feed.load_next()
    feed.load_next()
    assert len(feed.rendered) == 20
    assert feed.duplicates_rejected == 20
    assert len(feed.seen_ids) == 20


def test_tc015_last_partial_page_then_end():
    feed = ScrollFeed(PaginatedAPI(make_tasks(83), page_size=20))
    while feed.load_next():
        pass
    assert len(feed.rendered) == 83
    assert feed.rendered[-1].id == "T-083"
    assert feed.ended


def test_empty_feed_reaches_end_without_items():
    feed = ScrollFeed(PaginatedAPI(make_tasks(0), page_size=20))
    assert feed.load_next()
    assert feed.ended
    assert feed.rendered == []


def test_exact_multiple_total_hits_boundary():
    feed = ScrollFeed(PaginatedAPI(make_tasks(40), page_size=20))
    feed.load_next()
    feed.load_next()
    assert feed.ended
    assert len(feed.rendered) == 40


def test_total_just_above_multiple_loads_one_extra():
    feed = ScrollFeed(PaginatedAPI(make_tasks(41), page_size=20))
    feed.load_next()
    feed.load_next()
    feed.load_next()
    assert len(feed.rendered) == 41
    assert feed.ended
