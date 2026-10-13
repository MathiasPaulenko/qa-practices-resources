"""Mini paginated API for the pagination test cases companion.

Serves GET /items with two strategies:
- offset:  ?page=<1-indexed>&limit=<n>
- cursor:  ?limit=<n>&cursor=<base64 of last-seen id>

Run the tests with `pytest` — no server needed, they use the Flask test client.
"""

import base64
import json

from flask import Flask, jsonify, request

app = Flask(__name__)

ITEMS = []


def seed(n: int = 50) -> None:
    """Deterministic dataset; some items share created_at to test sort ties."""
    ITEMS.clear()
    ITEMS.extend(
        {
            "id": i,
            "name": f"item-{i:02d}",
            "status": "deleted" if i % 17 == 0 else "active",
            "created_at": "2026-10-01T10:00:00Z" if i % 3 == 0 else f"2026-10-{1 + i % 27:02d}T10:00:00Z",
        }
        for i in range(1, n + 1)
    )


def _sorted(items):
    # created_at first, id breaks ties — required for stable offset pagination
    return sorted(items, key=lambda x: (x["created_at"], x["id"]))


@app.get("/items")
def items():
    data = _sorted([i for i in ITEMS if request.args.get("status", None) in (None, i["status"])])
    limit = min(int(request.args.get("limit", 10)), 100)
    if limit < 1:
        return jsonify(error="limit must be >= 1"), 400

    cursor = request.args.get("cursor")
    if request.args.get("strategy") == "cursor" or cursor is not None:
        # cursor pagination: cursor = base64(last-seen id)
        last_id = 0
        if cursor:
            try:
                last_id = int(base64.b64decode(cursor).decode())
            except (ValueError, TypeError):
                return jsonify(error="Invalid cursor"), 400
        # cursor = keyset on id, so the cursor strategy sorts by id
        data = sorted((i for i in data if i["id"] > last_id), key=lambda x: x["id"])
        page = data[:limit]
        nxt = base64.b64encode(str(page[-1]["id"]).encode()).decode() if len(data) > limit else None
        return jsonify(items=page, nextCursor=nxt)

    page_no = int(request.args.get("page", 1))
    if page_no < 1:
        return jsonify(error="page must be >= 1"), 400
    start = (page_no - 1) * limit
    page = data[start : start + limit]
    total = len(data)
    total_pages = -(-total // limit)
    return jsonify(
        items=page,
        total=total,
        totalPages=total_pages,
        hasNextPage=page_no < total_pages,
    )


@app.post("/items")
def create_item():
    payload = request.get_json(force=True)
    new = {
        "id": max((i["id"] for i in ITEMS), default=0) + 1,
        "name": payload.get("name", "new-item"),
        "status": payload.get("status", "active"),
        "created_at": payload.get("created_at", "2026-10-01T10:00:00Z"),
    }
    ITEMS.append(new)
    return jsonify(new), 201


@app.post("/admin/reset")
def reset():
    seed()
    return jsonify(seeded=len(ITEMS))


seed()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
