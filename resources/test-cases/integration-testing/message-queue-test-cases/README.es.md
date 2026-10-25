# Casos de Prueba de Message Queue — Companion Ejecutable

Laboratorio local de RabbitMQ para los [Casos de Prueba de Message Queue](https://qapractices.com/es/test-cases/message-queue-test-cases/) en QAPractices.

## Contenido

- `docker-compose.yml` — RabbitMQ 3.13 con UI de gestión (localhost:15672, test/test).
- `ordering_test.py` — TC-001: publica 100 mensajes secuenciales y verifica el orden con un solo consumidor.
- `dlq_test.py` — TC-002: declara la topología DLX/DLQ y verifica que un mensaje venenoso llega a `orders.dlq`.

## Uso

```bash
docker compose up -d
pip install -r requirements.txt
python ordering_test.py && python dlq_test.py
```
