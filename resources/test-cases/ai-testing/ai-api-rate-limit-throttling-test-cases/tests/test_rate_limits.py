"""Pytest suite mapped to TC-01..TC-16 of ai-api-rate-limit-throttling-test-cases.

Runs entirely against the local FakeProvider — no real provider quota burned.
"""

import sys
import time
from pathlib import Path

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from client import call_with_backoff, iter_sse_events, parse_retry_after, stream_is_complete
from fake_provider import FakeProvider, ProviderConfig


@pytest.fixture()
def provider():
    cfg = ProviderConfig(window=60.0)
    p = FakeProvider(cfg).start()
    yield p
    p.stop()


@pytest.fixture()
def fast_provider():
    cfg = ProviderConfig(window=0.3)
    p = FakeProvider(cfg).start()
    yield p
    p.stop()


def post(provider, key="pro-key", model="small-model", max_tokens=1, headers=None):
    h = {"Authorization": f"Bearer {key}"}
    h.update(headers or {})
    return requests.post(provider.url, headers=h,
                         json={"model": model, "max_tokens": max_tokens}, timeout=10)


def test_tc01_request_within_limit(provider):
    resp = post(provider)
    assert resp.status_code == 200
    assert resp.json()["choices"][0]["finish_reason"] == "stop"
    assert int(resp.headers["x-ratelimit-remaining-requests"]) > 0


def test_tc02_requests_at_exact_boundary(provider):
    # pro-key tier allows 50 rpm; the model_rpm override caps small-model at 50 too
    for _ in range(50):
        assert post(provider).status_code == 200


def test_tc03_burst_limit_exceeded(provider):
    # small-model cap is 50 rpm
    for _ in range(50):
        assert post(provider).status_code == 200
    resp = post(provider)
    assert resp.status_code == 429
    assert "Retry-After" in resp.headers


def test_tc05_token_budget_exhaustion(provider):
    # free-key tpm = 200: two 150-token calls fit RPM but drain the token bucket
    assert post(provider, key="free-key", max_tokens=150).status_code == 200
    resp = post(provider, key="free-key", max_tokens=150)
    assert resp.status_code == 429
    assert "token" in resp.json()["error"]["message"].lower()


def test_tc06_retry_after_respected(provider):
    for _ in range(50):
        post(provider)
    resp = post(provider)
    wait = parse_retry_after(resp.headers["Retry-After"])
    assert wait is not None and wait >= 0


def test_tc06_retry_after_missing_uses_client_backoff():
    calls = []

    class FakeSession:
        def post(self, *a, **kw):
            class R:
                status_code = 429
                headers = {}
            return R()

    resp = call_with_backoff("http://x", {}, max_attempts=3, base_delay=1.0,
                             sleep=calls.append, session=FakeSession())
    assert resp.status_code == 429
    assert calls == [pytest.approx(d, rel=0.3) for d in (1.0, 2.0, 4.0)]


def test_tc07_backoff_grows_exponentially_with_jitter():
    first_waits = []

    class FakeSession:
        def post(self, *a, **kw):
            class R:
                status_code = 429
                headers = {}
            return R()

    # 20 simulated clients: base delay 1.0 + jitter spread means first retries
    # must NOT all land at the same instant
    for _ in range(20):
        call_with_backoff("http://x", {}, max_attempts=1, base_delay=1.0,
                          sleep=first_waits.append, session=FakeSession())
    assert all(1.0 <= w < 1.26 for w in first_waits)
    assert max(first_waits) - min(first_waits) > 0.01


def test_tc08_max_retry_limit_returns_terminal():
    attempts = []

    class FakeSession:
        def post(self, *a, **kw):
            attempts.append(1)
            class R:
                status_code = 429
                headers = {"Retry-After": "0"}
            return R()

    resp = call_with_backoff("http://x", {}, max_attempts=5, sleep=lambda s: None,
                             session=FakeSession())
    assert resp.status_code == 429
    assert len(attempts) == 5


def test_tc10_limits_differ_per_key(provider):
    # free-key rpm = 5, pro-key = 50
    for _ in range(5):
        assert post(provider, key="free-key").status_code == 200
    assert post(provider, key="free-key").status_code == 429
    assert post(provider, key="pro-key").status_code == 200


def test_tc11_model_specific_limits(provider):
    # big-model capped at 2 rpm, small-model at 50 — same key
    for _ in range(2):
        assert post(provider, model="big-model").status_code == 200
    assert post(provider, model="big-model").status_code == 429
    assert post(provider, model="small-model").status_code == 200


def test_tc12_streaming_truncation_detected():
    partial = ["data: {\"delta\": \"Hel", "data: {\"delta\": \"lo\""]
    complete = ["data: {\"delta\": \"Hi\"}", "data: [DONE]"]
    assert not stream_is_complete(list(iter_sse_events(partial)))
    assert stream_is_complete(list(iter_sse_events(complete)))


def test_tc13_graceful_degradation_fallback_model(provider):
    for _ in range(2):
        assert post(provider, model="big-model").status_code == 200
    primary = post(provider, model="big-model")
    assert primary.status_code == 429
    fallback = post(provider, model="small-model")
    assert fallback.status_code == 200


def test_tc14_overload_code_is_throttling(provider):
    resp = post(provider, headers={"X-Force-Status": "529"})
    assert resp.status_code == 529


def test_tc15_rate_limit_headers_present(provider):
    resp = post(provider)
    for name in ("x-ratelimit-limit-requests", "x-ratelimit-remaining-requests",
                 "x-ratelimit-reset-requests", "x-ratelimit-limit-tokens",
                 "x-ratelimit-remaining-tokens"):
        assert name in resp.headers


def test_tc16_quota_reset_behavior(fast_provider):
    # fast window: 300ms — exhaust small-model... cap is 50, use big-model cap 2
    assert post(fast_provider, model="big-model").status_code == 200
    assert post(fast_provider, model="big-model").status_code == 200
    assert post(fast_provider, model="big-model").status_code == 429
    time.sleep(0.4)
    assert post(fast_provider, model="big-model").status_code == 200


def test_edge_retry_after_http_date():
    from email.utils import formatdate
    value = formatdate(time.time() + 3, usegmt=True)
    wait = parse_retry_after(value)
    assert wait is not None and 2.0 < wait <= 3.0


def test_edge_daily_quota_returns_403(provider):
    # isolate the daily cap from TPM: wide-open tpm, tiny daily
    provider.config.key_tiers["free-key"] = {"rpm": 50, "tpm": 10000, "daily": 300}
    assert post(provider, key="free-key", max_tokens=200).status_code == 200
    resp = post(provider, key="free-key", max_tokens=200)
    assert resp.status_code == 403
    assert "quota" in resp.json()["error"]["type"]
