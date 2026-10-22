"""Tests for the in-memory broker — each maps to a concept in the guide."""

import pytest

from broker import Broker, Event, IdempotentHandler, ReadModel


def make_broker(partitions=3):
    b = Broker()
    t = b.create_topic("payments.processed", partitions=partitions)
    return b, t


def drain(group, consumer, handler):
    ev = consumer.poll()
    while ev is not None:
        consumer.process(handler, ev)
        ev = consumer.poll()


# --- ordering & partitioning ---------------------------------------------

def test_same_key_stays_in_partition_and_order():
    b, t = make_broker()
    p = b.publish(Event("payments.processed", "order-A", {"n": 1}))
    b.publish(Event("payments.processed", "order-A", {"n": 2}))
    b.publish(Event("payments.processed", "order-B", {"n": 9}))
    a_events = t.logs[t.partition_of("order-A")]
    assert [e.payload["n"] for e in a_events] == [1, 2]


def test_partition_spread_across_keys():
    b, t = make_broker()
    for i in range(12):
        b.publish(Event("payments.processed", f"k{i}", {"i": i}))
    used = sum(1 for log in t.logs if log)
    assert used > 1  # distribution over partitions


# --- at-least-once & idempotency ------------------------------------------

def test_duplicate_delivery_applied_once_with_dedup():
    b, t = make_broker()
    g = b.group("payments.processed", "g1")
    c = g.join("c1")
    charges = []
    handler = IdempotentHandler(lambda e: charges.append(e.payload["amount"]))
    ev = Event("payments.processed", "order-A", {"amount": 49.99}, "corr-1")
    b.publish(ev)
    b.publish(ev)  # duplicate — at-least-once delivers both
    drain(g, c, handler)
    assert len(c.processed) == 2      # broker delivers both
    assert charges == [49.99]         # but the side effect runs once


def test_consumer_without_dedup_applies_twice():
    b, t = make_broker()
    g = b.group("payments.processed", "g1")
    c = g.join("c1")
    charges = []
    ev = Event("payments.processed", "order-A", {"amount": 10}, "corr-2")
    b.publish(ev)
    b.publish(ev)
    drain(g, c, lambda e: charges.append(e.payload["amount"]))
    assert charges == [10, 10]        # the classic double-charge bug


# --- offsets & rebalancing ------------------------------------------------

def test_offset_commits_only_after_success():
    b, t = make_broker()
    g = b.group("payments.processed", "g1")
    c = g.join("c1")
    c.max_retries = 10  # keep retrying, never DLQ
    b.publish(Event("payments.processed", "k", {"ok": True}))
    calls = {"n": 0}
    def flaky(e):
        calls["n"] += 1
        if calls["n"] < 2:
            raise RuntimeError("transient")
    ev = c.poll()
    assert not c.process(flaky, ev)
    # retry succeeds on the second pass
    assert c.process(flaky, ev)
    assert c.processed == [ev]


def test_rebalance_redistributes_partitions_without_loss():
    b, t = make_broker(partitions=3)
    g = b.group("payments.processed", "g1")
    c1 = g.join("c1")
    assert len(c1.partitions) == 3
    c2 = g.join("c2")
    assert sorted(c1.partitions + c2.partitions) == [0, 1, 2]
    g.leave("c1")
    assert sorted(c2.partitions) == [0, 1, 2]


# --- DLQ & poison messages ------------------------------------------------

def test_poison_message_routes_to_dlq_after_retries():
    b, t = make_broker()
    g = b.group("payments.processed", "g1")
    c = g.join("c1")
    c.max_retries = 3
    poison = Event("payments.processed", "k", {"bad": "<not-json"})
    good = Event("payments.processed", "k", {"good": True})
    b.publish(poison)
    b.publish(good)
    def handler(e):
        if "bad" in e.payload:
            raise ValueError("unparseable")
    for _ in range(c.max_retries):
        c.process(handler, poison)
    c.process(handler, good)
    assert b.dlq == [poison]
    assert c.processed == [good]


def test_lag_grows_when_consumer_stalls():
    b, t = make_broker()
    g = b.group("payments.processed", "g1")
    g.join("c1")
    for i in range(7):
        b.publish(Event("payments.processed", "k", {"i": i}))
    assert g.lag() == 7  # alert threshold test: lag == published


# --- retention ------------------------------------------------------------

def test_retention_drops_oldest_messages():
    b = Broker()
    t = b.create_topic("tiny", partitions=1, retention=3)
    for i in range(5):
        b.publish(Event("tiny", "k", {"i": i}))
    remaining = [e.payload["i"] for e in t.logs[0]]
    assert remaining == [2, 3, 4]  # oldest two lost — past retention


# --- CQRS convergence -----------------------------------------------------

def test_read_model_converges_after_poll():
    b, t = make_broker()
    g = b.group("payments.processed", "g1")
    c = g.join("c1")
    rm = ReadModel()
    b.publish(Event("payments.processed", "order-A", {"paid": True}))
    # poll until converged — the CQRS SLA check from the guide
    attempts = 0
    while attempts < 5:
        ev = c.poll()
        if ev:
            c.process(rm.apply, ev)
        if rm.converged("order-A", {"paid": True}):
            break
        attempts += 1
    assert rm.converged("order-A", {"paid": True})
