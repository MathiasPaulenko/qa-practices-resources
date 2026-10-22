# Testing de Arquitectura Event-Driven — Companion

Companion de [Cómo Probar Arquitectura Event-Driven: Kafka, CQRS y Sagas](https://qapractices.com/es/documentation/event-driven-architecture-testing/) ([English version](https://qapractices.com/documentation/event-driven-architecture-testing/)).

## Qué incluye

- `broker.py` — un broker en memoria solo-stdlib que modela las piezas que los tests de EDA ejercitan: topics con particiones, consumer groups con offsets, rebalancing con assignor range, reentrega at-least-once, routing de poison messages a DLQ tras N reintentos, ventanas de retención y consumer lag — más `IdempotentHandler` (dedup por correlation_id) y un `ReadModel` para chequeos de convergencia CQRS.
- `tests/test_broker.py` — suite pytest que cubre orden dentro de una partición, entrega duplicada aplicada una vs dos veces, commits de offset tras éxito, rebalance sin pérdida, routing a DLQ, pérdida por retención, lag y convergencia del read model.

## Ejecutar

```bash
pip install -r requirements.txt
pytest tests/
```

## Notas

- El broker es un modelo didáctico, no un reemplazo de Kafka — reproduce las *semánticas* bajo prueba (scope de orden, at-least-once, retención) sin Docker.
- Para la versión con broker real, el artículo muestra un test de Testcontainers + `kafka-python` — `testcontainers[kafka]==4.7.3`, `kafka-python==2.0.2`, `pytest==8.3.3`.
