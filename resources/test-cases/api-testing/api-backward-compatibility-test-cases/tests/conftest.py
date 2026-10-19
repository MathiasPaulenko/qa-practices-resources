import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

PORT = 8571
BASE = f"http://127.0.0.1:{PORT}"
HEADERS = {"Authorization": "Bearer test-token"}


@pytest.fixture(scope="session")
def server():
    proc = subprocess.Popen(
        [sys.executable, str(Path(__file__).parent.parent / "mock_server.py"), str(PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(50):
        try:
            socket.create_connection(("127.0.0.1", PORT), timeout=0.5).close()
            break
        except OSError:
            time.sleep(0.1)
    else:
        proc.kill()
        raise RuntimeError("mock server did not start")
    yield BASE
    proc.terminate()
    proc.wait(timeout=5)
