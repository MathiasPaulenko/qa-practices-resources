"""Tests for webhook_client: backoff, Retry-After, DLQ routing and replay."""

import pytest
import requests
import responses

from webhook_client import DLQ, deliver_webhook

URL = "https://receiver.acme-corp.io/webhook"
PAYLOAD = {"event": "order.created", "order_id": 42}


@pytest.fixture
def dlq():
    return DLQ()


@pytest.fixture
def recorded_sleep(monkeypatch):
    delays = []

    def fake_sleep(seconds):
        delays.append(seconds)

    monkeypatch.setattr("webhook_client.time.sleep", fake_sleep)
    monkeypatch.setattr("webhook_client.random.uniform", lambda a, b: 0.0)
    return delays


@responses.activate
def test_delivers_on_first_attempt(dlq, recorded_sleep):
    responses.add(responses.POST, URL, status=200)
    assert deliver_webhook(URL, PAYLOAD, "evt_1", dlq) == "delivered"
    assert recorded_sleep == []
    assert dlq.messages == []


@responses.activate
def test_500_retries_with_backoff_then_dlq(dlq, recorded_sleep):
    responses.add(responses.POST, URL, status=500)
    result = deliver_webhook(URL, PAYLOAD, "evt_2", dlq, max_retries=4)
    assert result == "dlq"
    assert recorded_sleep == [1.0, 2.0, 4.0, 8.0]
    assert dlq.messages[0].reason == "max_retries"
    assert dlq.messages[0].attempts == 5


@responses.activate
def test_permanent_400_goes_straight_to_dlq(dlq, recorded_sleep):
    responses.add(responses.POST, URL, status=400)
    assert deliver_webhook(URL, PAYLOAD, "evt_3", dlq) == "dlq"
    assert recorded_sleep == []
    assert dlq.messages[0].reason == "permanent_400"


@responses.activate
def test_429_honors_retry_after(dlq, monkeypatch):
    responses.add(responses.POST, URL, status=429, headers={"Retry-After": "10"})
    responses.add(responses.POST, URL, status=200)
    delays = []
    monkeypatch.setattr("webhook_client.time.sleep", delays.append)
    monkeypatch.setattr("webhook_client.random.uniform", lambda a, b: 0.0)
    assert deliver_webhook(URL, PAYLOAD, "evt_4", dlq) == "delivered"
    assert delays[0] >= 10.0


@responses.activate
def test_timeout_counts_as_retriable(dlq, recorded_sleep):
    responses.add(responses.POST, URL, body=requests.ConnectionError("refused"))
    responses.add(responses.POST, URL, status=200)
    assert deliver_webhook(URL, PAYLOAD, "evt_5", dlq) == "delivered"
    assert len(recorded_sleep) == 1


@responses.activate
def test_replay_resends_with_original_event_id(dlq, monkeypatch):
    responses.add(responses.POST, URL, status=500)
    deliver_webhook(URL, PAYLOAD, "evt_6", dlq, max_retries=0)
    assert len(dlq.messages) == 1

    responses.reset()
    responses.add(responses.POST, URL, status=200)
    seen = {}

    def deliver(payload, event_id):
        seen["event_id"] = event_id
        import requests
        return "delivered" if requests.post(URL, json=payload).ok else "failed"

    assert dlq.replay("evt_6", deliver) == "delivered"
    assert seen["event_id"] == "evt_6"
    assert dlq.messages == []


@responses.activate
def test_dlq_rejects_duplicate_event_id(dlq, monkeypatch):
    responses.add(responses.POST, URL, status=500)
    deliver_webhook(URL, PAYLOAD, "evt_7", dlq, max_retries=0)
    deliver_webhook(URL, PAYLOAD, "evt_7", dlq, max_retries=0)
    assert len(dlq.messages) == 1
