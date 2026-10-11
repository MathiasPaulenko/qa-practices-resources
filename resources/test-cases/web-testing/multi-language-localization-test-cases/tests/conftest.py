import socket
import subprocess
import sys
import time

import pytest
import requests


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def api_base():
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, "mock_server.py", str(port)],
        cwd=".",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    base = f"http://127.0.0.1:{port}"
    for _ in range(50):
        try:
            requests.get(f"{base}/api/v1/locales", timeout=0.2)
            break
        except requests.RequestException:
            time.sleep(0.1)
    else:
        proc.kill()
        pytest.fail("mock server did not start")
    yield base
    proc.terminate()
