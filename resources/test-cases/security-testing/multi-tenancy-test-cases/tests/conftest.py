import socket
import subprocess
import sys
import time

import pytest
import requests

from mock_server import fake_jwt


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def api_base():
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, "-c", "from mock_server import Handler; from http.server import ThreadingHTTPServer; ThreadingHTTPServer(('127.0.0.1', %d), Handler).serve_forever()" % port],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    base = f"http://127.0.0.1:{port}"
    for _ in range(50):
        try:
            requests.get(f"{base}/api/health", timeout=0.2)
            break
        except requests.RequestException:
            time.sleep(0.1)
    else:
        proc.kill()
        pytest.fail("mock server did not start")
    yield base
    proc.terminate()


@pytest.fixture(scope="session")
def token_a():
    return fake_jwt("acme", "u-42")


@pytest.fixture(scope="session")
def token_b():
    return fake_jwt("globex", "u-77")
