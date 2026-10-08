"""Minimal GraphQL-over-HTTP mock for graphql-mutation-testing-test-cases.

Implements just enough mutation semantics to exercise the companion suite:
non-null validation, enum domain checks, batch partial failure,
authorization codes, error unions, idempotency-key replay and
optimistic concurrency. State lives in memory.

Stdlib only — run:  python mock_server.py [port]
"""
import asyncio
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

USERS = {}
NEXT_ID = [1]
IDEMPOTENCY_KEYS = set()
IDEMPOTENCY_CACHE = {}
SUBSCRIBERS = set()
WS_LOOP = None

WRITE_TOKEN = 'write-token'
READ_TOKEN = 'read-token'
VALID_ROLES = ('ADMIN', 'USER')
BATCH_LIMIT = 100


def user_view(u):
    return {'id': u['id'], 'email': u['email'], 'role': u['role'],
            'displayName': u['displayName'], 'version': u['version']}


def gql_error(code, message):
    return {'message': message, 'extensions': {'code': code}}


def create_user(input_data):
    uid = f'usr_{NEXT_ID[0]:04d}'
    NEXT_ID[0] += 1
    USERS[uid] = {'id': uid, 'email': input_data['email'],
                  'role': input_data.get('role', 'USER'),
                  'displayName': input_data.get('displayName'),
                  'version': 1}
    return USERS[uid]


def handle_create(variables):
    input_data = variables.get('input') or {}
    if input_data.get('email') is None:
        return {'errors': [gql_error('BAD_USER_INPUT',
                'Field "CreateUserInput.email" of required type "String!" was not provided.')]}
    role = input_data.get('role')
    if role is not None and role not in VALID_ROLES:
        return {'errors': [gql_error('BAD_USER_INPUT',
                f'Value "{role}" does not exist in "Role" enum.')]}
    if '@' not in input_data['email']:
        # Field-level validation surfaces through the payload union,
        # not the top-level errors array.
        return {'data': {'createUser': {'__typename': 'ValidationError',
                'field': 'email', 'message': 'Invalid email format'}}}
    return {'data': {'createUser': user_view(create_user(input_data))}}


def handle_batch(variables):
    users = variables.get('users') or []
    if len(users) > BATCH_LIMIT:
        return {'errors': [gql_error('BAD_USER_INPUT',
                f'Batch size {len(users)} exceeds limit of {BATCH_LIMIT}')]}
    results = []
    for item in users:
        email = item.get('email')
        if not email or '@' not in email:
            results.append({'email': email, 'ok': False, 'error': 'invalid email'})
        else:
            create_user(item)
            results.append({'email': email, 'ok': True, 'error': None})
    return {'data': {'createUsers': results}}


def handle_update(variables):
    uid = str(variables.get('id'))
    u = USERS.get(uid)
    if not u:
        return {'errors': [gql_error('NOT_FOUND', f'User {uid} not found')],
                'data': {'updateUser': None}}
    if 'version' in variables and variables['version'] is not None \
            and variables['version'] != u['version']:
        return {'errors': [gql_error('STALE_VERSION',
                f"Expected version {u['version']}, got {variables['version']}")],
                'data': {'updateUser': None}}
    for key in ('email', 'role', 'displayName'):
        if key in (variables.get('input') or {}):
            u[key] = variables['input'][key]
    u['version'] += 1
    publish({'type': 'userUpdated', 'payload': user_view(u)})
    return {'data': {'updateUser': user_view(u)}}


def handle_delete(variables):
    uid = str(variables.get('id'))
    if uid not in USERS:
        return {'errors': [gql_error('NOT_FOUND', f'User {uid} not found')],
                'data': {'deleteUser': None}}
    del USERS[uid]
    return {'data': {'deleteUser': {'success': True}}}


def dispatch(body, auth):
    """Naive operation dispatch by field name inside the query string."""
    query = body.get('query') or ''
    variables = body.get('variables') or {}
    if 'createUsers' in query:
        return handle_batch(variables)
    if 'createUser' in query:
        return handle_create(variables)
    if 'updateUser' in query:
        return handle_update(variables)
    if 'deleteUser' in query:
        if auth is None:
            return {'errors': [gql_error('UNAUTHENTICATED', 'Authentication required')]}
        if auth != WRITE_TOKEN:
            return {'errors': [gql_error('FORBIDDEN', 'Token scope is read-only')]}
        return handle_delete(variables)
    if 'user' in query:
        u = USERS.get(str(variables.get('id')))
        return {'data': {'user': user_view(u) if u else None}}
    return {'errors': [gql_error('BAD_REQUEST', 'Unknown operation')]}


def reset():
    USERS.clear()
    IDEMPOTENCY_KEYS.clear()
    IDEMPOTENCY_CACHE.clear()
    NEXT_ID[0] = 1


def publish(event):
    """Push a subscription event to every connected WebSocket client."""
    if WS_LOOP is None:
        return
    msg = json.dumps(event)
    for ws in list(SUBSCRIBERS):
        WS_LOOP.call_soon_threadsafe(
            lambda ws=ws: asyncio.ensure_future(ws.send(msg)))


async def _ws_handler(ws):
    SUBSCRIBERS.add(ws)
    try:
        async for _ in ws:
            pass
    finally:
        SUBSCRIBERS.discard(ws)


def run_ws(port=4001):
    """Subscription endpoint on a dedicated asyncio loop (needs `websockets`).

    Any client that connects receives `userUpdated` events as JSON whenever
    a mutation succeeds — enough to test TC-GQL-008.
    Returns (server, loop).
    """
    global WS_LOOP
    from websockets.asyncio.server import serve
    loop = asyncio.new_event_loop()
    WS_LOOP = loop

    async def _start():
        # serve() must run while the loop is running
        return await serve(_ws_handler, '127.0.0.1', port)

    server = loop.run_until_complete(_start())
    threading.Thread(target=loop.run_forever, daemon=True).start()
    return server, loop


class GraphQLHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/graphql':
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get('Content-Length') or 0)
        try:
            body = json.loads(self.rfile.read(length) or b'{}')
        except json.JSONDecodeError:
            body = {}
        auth = self.headers.get('Authorization')
        auth = auth.removeprefix('Bearer ').strip() if auth else None

        key = self.headers.get('Idempotency-Key')
        raw = json.dumps(body, sort_keys=True)
        if key and (key, raw) in IDEMPOTENCY_CACHE:
            payload = IDEMPOTENCY_CACHE[(key, raw)]  # replay: stored result
        elif key and key in IDEMPOTENCY_KEYS:
            payload = {'errors': [gql_error('IDEMPOTENCY_MISMATCH',
                       'Idempotency-Key reused with a different payload')]}
        else:
            payload = dispatch(body, auth)
            if key:
                IDEMPOTENCY_KEYS.add(key)
                IDEMPOTENCY_CACHE[(key, raw)] = payload

        data = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def run(port=4000):
    return HTTPServer(('127.0.0.1', port), GraphQLHandler)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    print(f'Mock GraphQL server on http://127.0.0.1:{port}/graphql')
    run(port).serve_forever()
