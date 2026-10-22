"""In-memory message broker for event-driven testing practice.

Models the pieces a QA needs to exercise without Docker: topics with
partitions, consumer groups with offsets, at-least-once redelivery,
dead-letter routing after N retries, and consumer lag — plus an
idempotent-consumer pattern keyed on correlation_id.

Companion to
https://qapractices.com/documentation/event-driven-architecture-testing/
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field


@dataclass
class Event:
    topic: str
    key: str
    payload: dict
    correlation_id: str = ""


class Topic:
    """A topic holds one ordered log per partition. Ordering is only
    guaranteed *inside* a partition — never across them."""

    def __init__(self, name: str, partitions: int = 3, retention: int = 100) -> None:
        self.name = name
        self.retention = retention  # max entries kept per partition
        self.logs: list[list[Event]] = [[] for _ in range(partitions)]

    def partition_of(self, key: str) -> int:
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return h % len(self.logs)

    def append(self, event: Event) -> int:
        p = self.partition_of(event.key)
        self.logs[p].append(event)
        if len(self.logs[p]) > self.retention:
            # Retention window: the oldest messages are gone for real.
            self.logs[p] = self.logs[p][-self.retention:]
        return p

    def read(self, partition: int, offset: int) -> Event | None:
        log = self.logs[partition]
        return log[offset] if 0 <= offset < len(log) else None

    def end_offset(self, partition: int) -> int:
        return len(self.logs[partition])


class Producer:
    def __init__(self, broker: "Broker") -> None:
        self.broker = broker

    def send(self, topic: str, key: str, payload: dict,
             correlation_id: str = "") -> int:
        return self.broker.publish(Event(topic, key, payload, correlation_id))


class Consumer:
    """Member of a consumer group. Reads in partition order; the caller
    decides *when* to commit — commit-before-process is how messages die."""

    def __init__(self, group: "ConsumerGroup", cid: str) -> None:
        self.group = group
        self.id = cid
        self.partitions: list[int] = []
        self.retries: dict[int, int] = {}
        self.max_retries = 3
        self.processed: list[Event] = []

    def assign(self, partitions: list[int]) -> None:
        self.partitions = partitions

    def poll(self) -> Event | None:
        for p in self.partitions:
            ev = self.group.topic.read(p, self.group.offset(p))
            if ev is not None:
                return ev
        return None

    def process(self, handler, event: Event) -> bool:
        """Runs the handler; on success commits the offset, on failure
        counts a retry — after max_retries the event goes to the DLQ."""
        p = self.group.topic.partition_of(event.key)
        try:
            handler(event)
        except Exception:
            n = self.retries.get(p, 0) + 1
            self.retries[p] = n
            if n >= self.max_retries:
                self.group.broker.dlq.append(event)
                self.retries[p] = 0
                self.group.commit(p)  # move past the poison message
            return False
        self.processed.append(event)
        self.group.commit(p)
        return True


class ConsumerGroup:
    def __init__(self, broker: "Broker", topic: Topic, name: str) -> None:
        self.broker = broker
        self.topic = topic
        self.name = name
        self._offsets = [0] * len(topic.logs)
        self.members: list[Consumer] = []

    def offset(self, partition: int) -> int:
        return self._offsets[partition]

    def commit(self, partition: int) -> None:
        self._offsets[partition] += 1

    def join(self, cid: str) -> Consumer:
        c = Consumer(self, cid)
        self.members.append(c)
        self._rebalance()
        return c

    def leave(self, cid: str) -> None:
        self.members = [m for m in self.members if m.id != cid]
        self._rebalance()

    def _rebalance(self) -> None:
        """Range assignor: contiguous partitions per member."""
        n = len(self.topic.logs)
        for i, m in enumerate(self.members):
            per = n // len(self.members)
            extra = n % len(self.members)
            start = i * per + min(i, extra)
            m.assign(list(range(start, start + per + (i < extra))))

    def lag(self) -> int:
        return sum(
            self.topic.end_offset(p) - self._offsets[p]
            for p in range(len(self.topic.logs))
        )


class Broker:
    def __init__(self) -> None:
        self.topics: dict[str, Topic] = {}
        self.dlq: list[Event] = []

    def create_topic(self, name: str, partitions: int = 3,
                     retention: int = 100) -> Topic:
        self.topics[name] = Topic(name, partitions, retention)
        return self.topics[name]

    def publish(self, event: Event) -> int:
        return self.topics[event.topic].append(event)

    def group(self, topic_name: str, name: str) -> ConsumerGroup:
        return ConsumerGroup(self, self.topics[topic_name], name)


class IdempotentHandler:
    """Consumer-side dedup keyed on correlation_id — the pattern the
    article recommends for at-least-once delivery."""

    def __init__(self, effect) -> None:
        self.seen: set[str] = set()
        self.effect = effect

    def __call__(self, event: Event) -> None:
        if event.correlation_id in self.seen:
            return
        self.seen.add(event.correlation_id)
        self.effect(event)


class ReadModel:
    """CQRS read side: converges asynchronously; test convergence by
    polling until the write is visible or a timeout expires."""

    def __init__(self) -> None:
        self.state: dict = {}

    def apply(self, event: Event) -> None:
        self.state[event.key] = event.payload

    def converged(self, key: str, expected: dict) -> bool:
        return self.state.get(key) == expected


def pretty(event: Event) -> str:
    return json.dumps(event.payload, sort_keys=True)
