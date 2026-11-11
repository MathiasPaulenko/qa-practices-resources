"""Cursor-based pagination helper — scales linearly unlike OFFSET.

The cursor is the last seen id: opaque to the client, a plain int
to the server. For opaque wire format, base64-encode it.
"""

import base64


def encode_cursor(last_id: int) -> str:
    return base64.b64encode(str(last_id).encode()).decode()


def decode_cursor(cursor: str | None) -> int:
    if not cursor:
        return 0
    return int(base64.b64decode(cursor.encode()).decode())


def paginate(rows: list[dict], cursor: str | None, limit: int = 50):
    """Return (page_rows, next_cursor) over id-sorted rows.

    Cursor pagination stays O(limit) regardless of depth — OFFSET
    degrades as O(n) because the database must count and skip rows.
    """
    last_id = decode_cursor(cursor)
    page = [r for r in rows if r["id"] > last_id][:limit]
    next_cursor = encode_cursor(page[-1]["id"]) if len(page) == limit else None
    return page, next_cursor
