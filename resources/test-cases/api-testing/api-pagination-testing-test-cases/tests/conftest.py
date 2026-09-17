import sys
import threading
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mock_server import PRODUCTS, run  # noqa: E402


@pytest.fixture(scope='session')
def base_url():
    server = run(port=0)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f'http://127.0.0.1:{port}'
    server.shutdown()


@pytest.fixture(autouse=True)
def reset_products():
    yield
    # Trim any products the tests inserted so each test sees the base 247.
    del PRODUCTS[247:]
