# Kafka Testing Guide — Companion Resources

Companion resources for the [Kafka Testing Guide: Real-Time Streams](https://qapractices.com/documentation/real-time-stream-testing-apache-kafka/) on QAPractices.com.

## Contents

| File | Description |
| --- | --- |
| `docker-compose.yml` | Single-node KRaft Kafka (`cp-kafka:7.6.0`) + Schema Registry (`cp-schema-registry:7.6.0`) for manual checks. |
| `KafkaOffsetResumeTest.java` | JUnit 5 + Testcontainers integration test: produces 100 records, commits offsets, restarts the consumer group and asserts no replay. |

## Requirements

- Docker (for both the compose stack and Testcontainers)
- Java 21, Maven 3.9 (for the JUnit test — add `testcontainers` 1.x `kafka` module and `kafka-clients` to your pom)

## Quick Start

Manual checks against a real broker:

```bash
docker compose up -d
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 3
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group order-consumers
```

JUnit test:

```bash
mvn test -Dtest=KafkaOffsetResumeTest
```
