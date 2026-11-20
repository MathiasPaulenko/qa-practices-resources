"""Minimal Prometheus instrumentation example (prometheus_client 0.26.0).

Exposes /metrics on :8000 and simulates request traffic so you can watch
counters and histograms move in Prometheus or Grafana.

Run:  pip install prometheus_client==0.26.0 && python prometheus-instrumentation.py
Then: curl http://localhost:8000/metrics
"""

import random
import time

from prometheus_client import Counter, Histogram, start_http_server

REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["endpoint"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5),
)


@REQUEST_DURATION.labels(endpoint="/api/users").time()
def handle_request() -> int:
    """Simulate a request; ~2% of calls fail so the error-rate panel moves."""
    time.sleep(random.uniform(0.01, 0.4))
    status = 500 if random.random() < 0.02 else 200
    REQUESTS_TOTAL.labels(method="GET", endpoint="/api/users", status=status).inc()
    return status


if __name__ == "__main__":
    start_http_server(8000)
    print("Metrics on http://localhost:8000/metrics — Ctrl+C to stop")
    while True:
        handle_request()
