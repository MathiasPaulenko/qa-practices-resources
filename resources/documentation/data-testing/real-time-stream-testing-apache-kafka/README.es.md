# Guía de Testing de Kafka — Recursos Complementarios

Recursos complementarios para la [Guía de Testing de Kafka: Streams en Tiempo Real](https://qapractices.com/es/documentation/real-time-stream-testing-apache-kafka/) en QAPractices.com.

## Contenido

| Archivo | Descripción |
| --- | --- |
| `docker-compose.yml` | Kafka KRaft de un nodo (`cp-kafka:7.6.0`) + Schema Registry (`cp-schema-registry:7.6.0`) para checks manuales. |
| `KafkaOffsetResumeTest.java` | Test de integración JUnit 5 + Testcontainers: produce 100 registros, commitea offsets, reinicia el consumer group y assertea que no hay replay. |

## Requisitos

- Docker (tanto para el stack de compose como para Testcontainers)
- Java 21, Maven 3.9 (para el test JUnit — agregá el módulo `kafka` de `testcontainers` 1.x y `kafka-clients` al pom)

## Inicio Rápido

Checks manuales contra un broker real:

```bash
docker compose up -d
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 3
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group order-consumers
```

Test JUnit:

```bash
mvn test -Dtest=KafkaOffsetResumeTest
```
