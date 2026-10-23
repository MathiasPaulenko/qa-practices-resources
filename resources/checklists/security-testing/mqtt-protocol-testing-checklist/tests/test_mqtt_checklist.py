"""Executable subset of the MQTT protocol testing checklist."""

import pytest

from mqtt_model import (
    Broker,
    RetainedStore,
    Session,
    WillMessage,
    effective_qos,
    on_disconnect,
    topic_match,
    validate_filter,
)


# --- Topic Structure and Filtering ---

def test_single_level_wildcard_matches_exactly_one_level():
    assert topic_match("home/+/temperature", "home/livingroom/temperature")
    assert not topic_match("home/+/temperature", "home/a/b/temperature")


def test_multi_level_wildcard_matches_all_remaining_levels():
    assert topic_match("sensors/#", "sensors/temperature/room1")
    assert topic_match("sensors/#", "sensors")
    assert not topic_match("sensors/#", "actuators/replay")


def test_malformed_filters_are_rejected():
    with pytest.raises(ValueError):
        validate_filter("home/#/temp")
    with pytest.raises(ValueError):
        validate_filter("sen+or/temp")
    with pytest.raises(ValueError):
        validate_filter("a/#/b")


def test_wildcards_never_match_dollar_prefixed_topics():
    assert not topic_match("#", "$SYS/broker/uptime")
    assert not topic_match("+/broker/uptime", "$SYS/broker/uptime")
    assert topic_match("$SYS/#", "$SYS/broker/uptime")


def test_oversized_filter_is_rejected():
    with pytest.raises(ValueError):
        validate_filter("a/" + "b" * 70_000)


# --- Quality of Service ---

def test_qos_downgrade_delivers_at_minimum():
    assert effective_qos(2, 1) == 1
    assert effective_qos(0, 2) == 0
    assert effective_qos(1, 1) == 1


def test_invalid_qos_rejected():
    with pytest.raises(ValueError):
        effective_qos(3, 1)


# --- Retained Messages ---

def test_last_retained_publish_wins():
    store = RetainedStore()
    store.publish("devices/d1/status", b"online", retain=True)
    store.publish("devices/d1/status", b"busy", retain=True)
    assert store.for_new_subscriber("devices/#") == {"devices/d1/status": b"busy"}


def test_empty_payload_with_retain_clears_message():
    store = RetainedStore()
    store.publish("devices/d1/status", b"online", retain=True)
    store.publish("devices/d1/status", b"", retain=True)
    assert store.for_new_subscriber("devices/#") == {}


def test_new_subscriber_gets_retained_for_matching_topics_only():
    store = RetainedStore()
    store.publish("sensors/temp/room1", b"23.5", retain=True)
    store.publish("actuators/door", b"open", retain=True)
    assert store.for_new_subscriber("sensors/#") == {"sensors/temp/room1": b"23.5"}


# --- Session Persistence ---

def test_persistent_session_redelivers_unacked_qos1():
    s = Session(persistent=True)
    s.queue("sensors/temp", b"23.5", qos=1)
    s.queue("sensors/hum", b"60", qos=0)  # qos0 is not stored
    pending = s.reconnect()
    assert len(pending) == 1 and pending[0]["qos"] == 1


def test_clean_session_discards_state_on_reconnect():
    s = Session(persistent=False)
    s.queue("sensors/temp", b"23.5", qos=1)
    s.subscriptions.append("sensors/#")
    assert s.reconnect() == []
    assert s.subscriptions == []


# --- Last Will and Testament ---

def test_lwt_fires_on_ungraceful_disconnect():
    will = WillMessage("devices/d1/status", b"offline", qos=1, retain=True)
    assert on_disconnect(will, graceful=False) is will


def test_lwt_not_fired_on_graceful_disconnect():
    will = WillMessage("devices/d1/status", b"offline", qos=1, retain=True)
    assert on_disconnect(will, graceful=True) is None


# --- Broker Connectivity ---

def test_duplicate_client_id_triggers_takeover():
    broker = Broker()
    first, second = object(), object()
    assert broker.connect("client-a", first) is None
    assert broker.connect("client-a", second) is first
    assert broker.clients["client-a"] is second
