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
        [sys.executable, "-c", "from mock_llm import Handler; from http.server import ThreadingHTTPServer; ThreadingHTTPServer(('127.0.0.1', %d), Handler).serve_forever()" % port],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    base = f"http://127.0.0.1:{port}"
    for _ in range(50):
        try:
            requests.post(f"{base}/reset", timeout=0.2)
            break
        except requests.RequestException:
            time.sleep(0.1)
    else:
        proc.kill()
        pytest.fail("mock LLM did not start")
    yield base
    proc.terminate()


@pytest.fixture(autouse=True)
def reset_state(api_base):
    requests.post(f"{api_base}/reset")


def chat(api_base, message, file_content=None):
    payload = {"message": message}
    if file_content is not None:
        payload["file_content"] = file_content
    return requests.post(f"{api_base}/chat", json=payload, timeout=5)
