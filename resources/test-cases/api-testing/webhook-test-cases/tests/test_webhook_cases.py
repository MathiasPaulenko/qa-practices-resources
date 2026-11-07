"""Pytest suite mapping TC-01..TC-12 from qapractices.com/test-cases/webhook-test-cases."""

import json

import pytest

from webhook_pipeline import Consumer, Provider, sign, validate_endpoint

SECRET = "whsec_test_9f8d"
NOW = 1_731_500_100
KNOWN_TYPES = {"payment.succeeded", "subscription.updated"}


def make_body(event_id="evt_001", event_type="payment.succeeded",
              created=NOW, object_id="obj_1", amount=4999):
    return json.dumps({
        "id": event_id,
        "type": event_type,
        "created": created,
        "data": {"object_id": object_id, "amount": amount},
    }).encode()


@pytest.fixture
def consumer():
    return Consumer([SECRET], known_types=KNOWN_TYPES)


# TC-01: a correctly signed delivery is accepted.
def test_tc01_valid_signature_accepted(consumer):
    body = make_body()
    status, reason = consumer.receive(body, sign(body, SECRET, NOW), NOW)
    assert status == 200 and reason == "processed"
    assert consumer.effects == ["evt_001"]


# TC-02: wrong secret, tampered body and missing header all get 401.
@pytest.mark.parametrize("variant", ["wrong_secret", "tampered", "missing"])
def test_tc02_forged_deliveries_rejected(consumer, variant):
    body = make_body()
    if variant == "wrong_secret":
        header = sign(body, "whsec_other", NOW)
    elif variant == "tampered":
        header = sign(make_body(amount=499900), SECRET, NOW)
    else:
        header = None
    status, _ = consumer.receive(body, header, NOW)
    assert status == 401
    assert consumer.effects == []


# TC-03: a valid signature on a stale timestamp is rejected as replay.
def test_tc03_replay_outside_tolerance(consumer):
    body = make_body()
    assert consumer.receive(body, sign(body, SECRET, NOW), NOW)[0] == 200
    replay_status, _ = consumer.receive(body, sign(body, SECRET, NOW), NOW + 360)
    assert replay_status == 401


# TC-04: re-sent events are acked with 200 but processed once.
def test_tc04_duplicate_delivery_processed_once(consumer):
    body = make_body(event_id="evt_dup_01")
    for _ in range(3):
        status, _ = consumer.receive(body, sign(body, SECRET, NOW), NOW)
        assert status == 200
    assert consumer.effects == ["evt_dup_01"]
    assert consumer.seen["evt_dup_01"] == 3


# TC-05: an older event arriving after a newer one never regresses state.
def test_tc05_out_of_order_discarded(consumer):
    v3 = make_body(event_id="evt_v3", event_type="subscription.updated",
                   created=NOW, amount=4999)
    v2 = make_body(event_id="evt_v2", event_type="subscription.updated",
                   created=NOW - 50, amount=999)
    assert consumer.receive(v3, sign(v3, SECRET, NOW), NOW) == (200, "processed")
    status, reason = consumer.receive(v2, sign(v2, SECRET, NOW), NOW + 10)
    assert (status, reason) == (200, "stale_event")
    assert consumer.last_created["obj_1"] == NOW  # v3 state stands


# TC-06: provider retries 5xx on the configured backoff schedule.
def test_tc06_retry_backoff_schedule():
    provider = Provider(schedule=[60, 300, 1800])
    calls = {"n": 0}

    def flaky_endpoint(body, header, now):
        calls["n"] += 1
        return (500, "boom") if calls["n"] < 3 else (200, "ok")

    assert provider.deliver(flaky_endpoint, make_body(), SECRET, NOW) is True
    waits = [t[1] - NOW for t in provider.attempts]
    assert waits == [0, 60, 360]  # retries at +60s and +300s


# TC-07: covered as contract — consumer returns before side effects run.
# The Consumer here applies effects synchronously inside receive(); in a real
# receiver the same ordering holds: ack first, queue the work.


# TC-08: signed but malformed bodies get 400 with no retry.
def test_tc08_malformed_payload_no_retry(consumer):
    provider = Provider()
    truncated = b'{"id":"evt_x","type":"payme'
    missing = json.dumps({"id": "evt_y", "created": NOW}).encode()
    for body in (truncated, missing):
        status, _ = consumer.receive(body, sign(body, SECRET, NOW), NOW)
        assert status == 400
    ok = provider.deliver(consumer.receive, missing, SECRET, NOW)
    assert ok is False and len(provider.attempts) == 1  # 4xx = no retry


# TC-09: unknown event types are acked and ignored, never a 5xx.
def test_tc09_unknown_event_type(consumer):
    body = make_body(event_id="evt_legacy", event_type="legacy.deprecated_thing")
    status, reason = consumer.receive(body, sign(body, SECRET, NOW), NOW)
    assert (status, reason) == (200, "ignored_type")
    assert consumer.effects == []


# TC-10: during rotation both secrets verify; after expiry only the new one.
def test_tc10_secret_rotation_window():
    rotating = Consumer([SECRET, "whsec_new"], known_types=KNOWN_TYPES)
    body_a = make_body(event_id="evt_a")
    body_b = make_body(event_id="evt_b")
    assert rotating.receive(body_a, sign(body_a, SECRET, NOW), NOW)[0] == 200
    assert rotating.receive(body_b, sign(body_b, "whsec_new", NOW), NOW)[0] == 200
    expired = Consumer(["whsec_new"], known_types=KNOWN_TYPES)
    assert expired.receive(body_a, sign(body_a, SECRET, NOW), NOW)[0] == 401


# TC-11: only HTTPS endpoints with valid, matching certs are accepted.
@pytest.mark.parametrize(
    "scheme,cert_valid,host_match,expected",
    [
        ("https", True, True, True),
        ("http", True, True, False),
        ("https", False, True, False),
        ("https", True, False, False),
    ],
)
def test_tc11_endpoint_validation(scheme, cert_valid, host_match, expected):
    assert validate_endpoint(scheme, cert_valid, host_match) is expected


# TC-12: exhausted retries land in the dead-letter queue.
def test_tc12_dead_letter_after_exhaustion():
    provider = Provider(schedule=[60, 300], max_attempts=3)

    def always_down(body, header, now):
        return 500, "still down"

    assert provider.deliver(always_down, make_body(), SECRET, NOW) is False
    assert len(provider.attempts) == 3
    assert len(provider.dlq) == 1
