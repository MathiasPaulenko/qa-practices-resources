# API Mocking and Stubbing Testing Checklist — Companion

Companion resource for [API Mocking and Stubbing Testing Checklist](https://qapractices.com/checklists/api-mocking-and-stubbing-testing-checklist).

A minimal runnable WireMock setup: one stub mapping, a Docker Compose service and a Python consumer test that validates both the mapped response and the 404 fallthrough.

## Contents

- `mappings/get-user-123.json` — WireMock 3.x stub mapping for `GET /users/123`
- `docker-compose.yml` — WireMock 3.13.2 container on port 8080
- `tests/test_mock_consumer.py` — consumer test with requests 2.32 and pytest 8.3
- `requirements.txt` — Python dependencies

## Requirements

- Docker with Compose
- Python 3.12+ with requests 2.32 and pytest 8.3

## Usage

```bash
# Start the mock server
docker compose up -d

# Verify the stub responds
curl http://localhost:8080/users/123

# Install deps and run the consumer tests
pip install -r requirements.txt
python -m pytest tests/ -v

# Stop the mock
docker compose down
```

## Extending

Drop more `.json` mappings under `mappings/` — WireMock picks them up on restart. Add fault-injection scenarios (`fixedDelayMilliseconds`, 5xx statuses) to cover the error-simulation section of the checklist.
