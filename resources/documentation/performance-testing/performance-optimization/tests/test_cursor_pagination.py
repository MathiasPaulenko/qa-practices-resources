"""Tests for the cursor pagination helper — stdlib only, no database."""

from src.cursor_pagination import decode_cursor, encode_cursor, paginate

ROWS = [{"id": i} for i in range(1, 101)]


def test_first_page_without_cursor():
    page, nxt = paginate(ROWS, None, limit=10)
    assert page[0]["id"] == 1
    assert page[-1]["id"] == 10
    assert nxt is not None


def test_second_page_continues_where_first_stopped():
    _, c1 = paginate(ROWS, None, limit=10)
    page, _ = paginate(ROWS, c1, limit=10)
    assert page[0]["id"] == 11


def test_last_page_has_no_next_cursor():
    _, c1 = paginate(ROWS, None, limit=10)
    page, nxt = paginate(ROWS, c1, limit=90)
    assert len(page) == 90
    assert nxt is None


def test_cursor_roundtrip():
    assert decode_cursor(encode_cursor(42)) == 42
    assert decode_cursor(None) == 0
