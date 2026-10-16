"""Payment security regression suite against the stdlib mock server.

Covers the attack scenarios from the guide: amount/currency tampering,
idempotent replay, forged webhook signatures and out-of-window replays.
"""

import pytest
import requests

from mock_payment_server import WEBHOOK_SECRET, sign_webhook, start_server
import mock_payment_server


@pytest.fixture()
def base_url():
    mock_payment_server.charges.clear()
    mock_payment_server.idempotency_index.clear()
    mock_payment_server.webhook_events.clear()
    server, port, _thread = start_server()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


def pay(url: str, **overrides) -> requests.Response:
    body = {
        "amount": 99.99,
        "currency": "USD",
        "paymentToken": "tok_visa_4242",
        "orderId": "ord_7f3a9c",
    }
    body.update(overrides)
    headers = {"Idempotency-Key": "idem-test-001"}
    return requests.post(f"{url}/api/checkout/pay", json=body, headers=headers, timeout=5)


def test_amount_tampering_is_rejected(base_url):
    response = pay(base_url, amount=0.01)
    assert response.status_code == 400
    assert response.json()["error"] == "amount mismatch"
    assert mock_payment_server.charges == []


def test_currency_tampering_is_rejected(base_url):
    response = pay(base_url, currency="JPY")
    assert response.status_code == 400
    assert mock_payment_server.charges == []


def test_idempotent_replay_creates_single_charge(base_url):
    first = pay(base_url)
    replay = pay(base_url)
    assert first.status_code == replay.status_code == 200
    assert first.json()["id"] == replay.json()["id"]
    assert len(mock_payment_server.charges) == 1


def test_forged_webhook_signature_is_rejected(base_url):
    payload = b'{"type":"payment.succeeded","orderId":"ord_7f3a9c"}'
    bad = f"t={__import__('time').time():.0f},v1={'0' * 64}"
    response = requests.post(
        f"{base_url}/webhooks/payments",
        data=payload,
        headers={"X-Payment-Signature": bad},
        timeout=5,
    )
    assert response.status_code == 401
    assert mock_payment_server.webhook_events == []


def test_replayed_webhook_outside_tolerance_is_rejected(base_url):
    import time

    stale = int(time.time()) - 3600
    payload = b'{"type":"payment.succeeded","orderId":"ord_7f3a9c"}'
    header = sign_webhook(payload, timestamp=stale)
    response = requests.post(
        f"{base_url}/webhooks/payments",
        data=payload,
        headers={"X-Payment-Signature": header},
        timeout=5,
    )
    assert response.status_code == 401


def test_valid_signed_webhook_is_accepted(base_url):
    payload = b'{"type":"payment.succeeded","orderId":"ord_7f3a9c"}'
    header = sign_webhook(payload)
    response = requests.post(
        f"{base_url}/webhooks/payments",
        data=payload,
        headers={"X-Payment-Signature": header},
        timeout=5,
    )
    assert response.status_code == 200
    assert len(mock_payment_server.webhook_events) == 1


def test_webhook_signed_with_wrong_secret_is_rejected(base_url):
    payload = b'{"type":"payment.succeeded"}'
    header = sign_webhook(payload, secret=b"whsec_attacker_controlled")
    response = requests.post(
        f"{base_url}/webhooks/payments",
        data=payload,
        headers={"X-Payment-Signature": header},
        timeout=5,
    )
    assert response.status_code == 401
    assert WEBHOOK_SECRET != b"whsec_attacker_controlled"
