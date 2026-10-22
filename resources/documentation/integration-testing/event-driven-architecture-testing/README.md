# Event-Driven Architecture Testing — Companion

Companion for [Event-Driven Architecture Testing: Kafka, CQRS and Sagas](https://qapractices.com/documentation/event-driven-architecture-testing/) ([versión en español](https://qapractices.com/es/documentation/event-driven-architecture-testing/)).

## What's inside

- `broker.py` — a stdlib-only in-memory broker modeling the pieces EDA tests exercise: topics with partitions, consumer groups with offsets, range-assignor rebalancing, at-least-once redelivery, poison-message routing to a DLQ after N retries, retention windows and consumer lag — plus `IdempotentHandler` (correlation_id dedup) and a `ReadModel` for CQRS convergence checks.
- `tests/test_broker.py` — pytest suite covering ordering within a partition, duplicate delivery applied once vs twice, offset commits after success, rebalance without loss, DLQ routing, retention drop, lag, and read-model convergence.

## Run

```bash
pip install -r requirements.txt
pytest tests/
```

## Notes

- The broker is a teaching model, not a Kafka replacement — it reproduces the *semantics* under test (ordering scope, at-least-once, retention) without Docker.
- For the real-broker version, the article shows a Testcontainers + `kafka-python` test — `testcontainers[kafka]==4.7.3`, `kafka-python==2.0.2`, `pytest==8.3.3`.
