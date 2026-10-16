import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from error_server import ErrorPageHandler, RATE_LIMIT_PER_MINUTE  # noqa: E402


@pytest.fixture(scope="session")
def base_url():
    server = ThreadingHTTPServer(("127.0.0.1", 0), ErrorPageHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    thread.join(timeout=5)


@pytest.fixture(autouse=True)
def reset_rate_limit():
    ErrorPageHandler._rate_counter = 0
    yield


@pytest.fixture(scope="session")
def rate_limit():
    return RATE_LIMIT_PER_MINUTE


@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    yield s
    s.close()
