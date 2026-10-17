"""Concurrent stock reservation test — companion for the inventory test cases resource.

Seed SKU123 with stock=1 on the target API, then run:

    API_BASE_URL=https://staging.yourstore.test/api pytest reservation_test.py -v

Invariant under test: with one unit available, exactly one of N concurrent
reservations may succeed. More than one 200 means overselling.
"""

import os
import threading
from queue import Queue

import pytest
import requests

BASE_URL = os.environ["API_BASE_URL"]
SKU = "SKU123"
WORKERS = 10


def reserve_stock(sku: str, results: "Queue[int]") -> None:
    response = requests.post(
        f"{BASE_URL}/api/reserve", json={"sku": sku, "qty": 1}, timeout=5
    )
    results.put(response.status_code)


def test_concurrent_reservation_prevents_oversell() -> None:
    results: "Queue[int]" = Queue()
    threads = [
        threading.Thread(target=reserve_stock, args=(SKU, results))
        for _ in range(WORKERS)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    statuses = [results.get() for _ in range(WORKERS)]
    assert statuses.count(200) == 1, f"Oversell detected: {statuses}"


def test_reservation_releases_after_timeout() -> None:
    """Second invariant: an abandoned reservation returns the unit to available."""
    pytest.skip(
        "Requires a configurable reservation TTL — set TTL low, reserve, "
        "wait, then assert the unit is available again."
    )
