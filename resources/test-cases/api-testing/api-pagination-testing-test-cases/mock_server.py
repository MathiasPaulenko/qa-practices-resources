"""Mock paginated API for the api-pagination-testing-test-cases companion.

Implements offset (?page&limit or ?offset&limit), cursor (?cursor&limit)
and keyset (?after_id&limit) pagination over an in-memory product list,
plus POST /products to simulate concurrent inserts mid-pagination.

Stdlib only — run:  python mock_server.py [port]
"""
import base64
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

PRODUCTS = [
    {
        'id': i,
        'name': f'product-{i:04d}',
        # Every 7th product shares a timestamp — lets tests exercise the
        # non-unique-sort-column + tiebreaker path (TC-10).
        'created_at': f'2026-09-{(i // 7) + 1:02d}T10:00:00Z',
        'status': 'active' if i % 4 else 'archived',
    }
    for i in range(1, 248)  # 247 products — last page of limit=10 has 7 items
]
NEXT_ID = [248]


def sort_key(p):
    # created_at DESC with id as documented tiebreaker
    return (-int(p['created_at'][8:10]), -p['id'])


def encode_cursor(product_id):
    return base64.urlsafe_b64encode(f'after:{product_id}'.encode()).decode()


def decode_cursor(cursor):
    try:
        raw = base64.urlsafe_b64decode(cursor.encode()).decode()
        kind, pid = raw.split(':', 1)
        return int(pid) if kind == 'after' else None
    except Exception:
        return None


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, code, msg):
        self._send(code, {'error': msg})

    def _parse_limit(self, q):
        raw = q.get('limit', ['20'])[0]
        try:
            limit = int(raw)
        except ValueError:
            return None, 'limit must be an integer'
        if limit < 1:
            return None, 'limit must be between 1 and 100'
        if limit > 100:
            return None, 'limit exceeds maximum of 100'
        return limit, None

    def _filtered(self, q):
        rows = sorted(PRODUCTS, key=sort_key)
        status = q.get('status', [None])[0]
        if status:
            rows = [r for r in rows if r['status'] == status]
        return rows

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != '/products':
            return self._error(404, 'not found')
        q = parse_qs(parsed.query)
        rows = self._filtered(q)
        total = len(rows)

        limit, err = self._parse_limit(q)
        if err:
            return self._error(400, err)

        # Cursor / keyset mode
        if 'cursor' in q or 'after_id' in q:
            if 'cursor' in q:
                after = decode_cursor(q['cursor'][0])
                if after is None:
                    return self._error(400, 'Invalid or expired cursor')
            else:
                try:
                    after = int(q['after_id'][0])
                except ValueError:
                    return self._error(400, 'after_id must be an integer')
            start = next((i for i, r in enumerate(rows) if r['id'] == after), -1) + 1
            page = rows[start:start + limit]
            last = page[-1]['id'] if page else after
            return self._send(200, {
                'data': page,
                'limit': limit,
                'total_count': total,
                'has_next_page': start + limit < total,
                'next_cursor': encode_cursor(last) if start + limit < total else None,
            })

        # Offset mode (?page or ?offset)
        if 'page' in q:
            try:
                page_n = int(q['page'][0])
            except ValueError:
                return self._error(400, 'page must be an integer')
            if page_n < 1:
                return self._error(400, 'page must be >= 1')
            offset = (page_n - 1) * limit
        else:
            try:
                offset = int(q.get('offset', ['0'])[0])
            except ValueError:
                return self._error(400, 'offset must be an integer')
            if offset < 0:
                return self._error(400, 'offset must be >= 0')
            page_n = offset // limit + 1

        page = rows[offset:offset + limit]
        has_next = offset + limit < total
        self._send(200, {
            'data': page,
            'page': page_n,
            'limit': limit,
            'total_count': total,
            'has_next_page': has_next,
            'next_cursor': encode_cursor(page[-1]['id']) if has_next and page else None,
        })

    def do_POST(self):
        if urlparse(self.path).path != '/products':
            return self._error(404, 'not found')
        length = int(self.headers.get('Content-Length', 0))
        payload = json.loads(self.rfile.read(length) or b'{}')
        pid = NEXT_ID[0]
        NEXT_ID[0] += 1
        product = {
            'id': pid,
            'name': payload.get('name', f'product-{pid:04d}'),
            'created_at': payload.get('created_at', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())),
            'status': payload.get('status', 'active'),
        }
        PRODUCTS.append(product)
        self._send(201, product)

    def log_message(self, *args):
        pass  # quiet


def run(port=0):
    server = HTTPServer(('127.0.0.1', port), Handler)
    return server


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8571
    print(f'mock paginated API on http://127.0.0.1:{port}/products')
    run(port).serve_forever()
