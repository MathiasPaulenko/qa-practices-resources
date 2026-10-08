import sys
import threading
from pathlib import Path

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mock_server import reset, run, run_ws  # noqa: E402

CREATE = """
mutation($input: CreateUserInput!) {
  createUser(input: $input) { id email role displayName version }
}
"""

CREATE_UNION = """
mutation($input: CreateUserInput!) {
  createUser(input: $input) {
    ... on User { id email }
    ... on ValidationError { field message }
  }
}
"""

UPDATE = """
mutation($id: ID!, $version: Int, $input: UpdateUserInput!) {
  updateUser(id: $id, version: $version, input: $input) {
    id email role displayName version
  }
}
"""

DELETE = """
mutation($id: ID!) {
  deleteUser(id: $id) { success }
}
"""

BATCH = """
mutation($users: [CreateUserInput!]!) {
  createUsers(input: $users) { email ok error }
}
"""

GET = """
query($id: ID!) {
  user(id: $id) { id email role displayName version }
}
"""

WRITE_AUTH = {'Authorization': 'Bearer write-token'}
READ_AUTH = {'Authorization': 'Bearer read-token'}


def graphql(base_url, query, variables=None, headers=None):
    merged = {'Content-Type': 'application/json'}
    merged.update(headers or {})
    response = requests.post(
        f'{base_url}/graphql',
        json={'query': query, 'variables': variables or {}},
        headers=merged,
        timeout=10,
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope='session')
def base_url():
    server = run(port=0)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f'http://127.0.0.1:{port}'
    server.shutdown()


@pytest.fixture(scope='session')
def ws_url():
    websockets = pytest.importorskip('websockets')
    del websockets  # presence check only
    server, loop = run_ws(port=0)
    port = server.sockets[0].getsockname()[1]
    yield f'ws://127.0.0.1:{port}'
    loop.call_soon_threadsafe(loop.stop)


@pytest.fixture(autouse=True)
def clean_state():
    yield
    reset()
