import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mock_server import reset_store, start_server  # noqa: E402


@pytest.fixture()
def api():
    """Run the mock on an ephemeral port and yield its base URL."""
    server = start_server(port=0)
    base = "http://127.0.0.1:%d" % server.server_address[1]
    reset_store()
    yield base
    server.shutdown()
