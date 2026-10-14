import sys
import threading
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mock_server import Handler, reset_store  # noqa: E402
from http.server import ThreadingHTTPServer  # noqa: E402


@pytest.fixture()
def server():
    reset_store()
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield "http://127.0.0.1:%d" % httpd.server_port
    httpd.shutdown()
    thread.join(timeout=5)
