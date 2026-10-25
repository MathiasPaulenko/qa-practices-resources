# Message Queue Test Cases — Runnable Companion

Local RabbitMQ lab for the [Message Queue Test Cases](https://qapractices.com/test-cases/message-queue-test-cases/) on QAPractices.

## Contents

- `docker-compose.yml` — RabbitMQ 3.13 with management UI (localhost:15672, test/test).
- `ordering_test.py` — TC-001: publishes 100 sequential messages, asserts single-consumer ordering.
- `dlq_test.py` — TC-002: declares a DLX/DLQ topology and verifies a poison message lands in `orders.dlq`.

## Usage

```bash
docker compose up -d
pip install -r requirements.txt
python ordering_test.py && python dlq_test.py
```
