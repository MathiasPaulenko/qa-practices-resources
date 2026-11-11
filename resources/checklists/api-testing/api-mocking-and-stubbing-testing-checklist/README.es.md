# Checklist de API Mocking y Stubbing — Companion

Recurso companion de [Checklist de API Mocking y Stubbing](https://qapractices.com/es/checklists/api-mocking-and-stubbing-testing-checklist).

Setup de WireMock mínimo y ejecutable: un mapping de stub, un servicio Docker Compose y un test de consumidor en Python que valida la respuesta mapeada y el fallthrough 404.

## Contenido

- `mappings/get-user-123.json` — mapping de stub WireMock 3.x para `GET /users/123`
- `docker-compose.yml` — contenedor WireMock 3.13.2 en el puerto 8080
- `tests/test_mock_consumer.py` — test de consumidor con requests 2.32 y pytest 8.3
- `requirements.txt` — dependencias de Python

## Requisitos

- Docker con Compose
- Python 3.12+ con requests 2.32 y pytest 8.3

## Uso

```bash
# Levantar el mock server
docker compose up -d

# Verificar que el stub responde
curl http://localhost:8080/users/123

# Instalar dependencias y correr los tests de consumidor
pip install -r requirements.txt
python -m pytest tests/ -v

# Apagar el mock
docker compose down
```

## Extender

Añade más mappings `.json` en `mappings/` — WireMock los recoge al reiniciar. Agrega escenarios de inyección de fallos (`fixedDelayMilliseconds`, estados 5xx) para cubrir la sección de simulación de errores del checklist.
