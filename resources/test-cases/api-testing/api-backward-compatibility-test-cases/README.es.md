# Compatibilidad Backward de API — Companion Ejecutable

Companion ejecutable de la guía [Casos de Prueba de Compatibilidad de API: TaskFlow](https://qapractices.com/es/test-cases/api-backward-compatibility-test-cases/) en QAPractices.

Un mock server stdlib implementa el contrato de versionado de TaskFlow descrito en la guía — negociación por header `API-Version`, la división de esquema `2025-01`/`2026-07` (`assignee_id` → `assignee`), los headers `Deprecation`/`Sunset` (RFC 9745 / RFC 8594) y una versión retirada `2024-03` que responde `410 Gone`. Una suite de pytest 8.3 ejercita los mismos casos que las tablas de la guía.

## Contenido

- `mock_server.py` — la fixture TaskFlow: versionado por header, campo deprecado en dual, validación de enum, headers de rate limit, enforcement del sunset
- `tests/test_version_negotiation.py` — TC-001 a TC-004: contrato viejo/nuevo, default sin header, versión no soportada
- `tests/test_field_compatibility.py` — TC-005 a TC-007 + filas edge: campo en dual, borde de campo opcional, enum eliminado, mapeo de escritura de cliente viejo
- `tests/test_deprecation_sunset.py` — TC-016: `410 Gone` con `Link: rel="successor-version"`, header `Sunset` en la versión estable
- `tests/test_contract_stability.py` — TC-008/010/013/014/015: paginación, forma de error, métodos HTTP, auth y headers de rate limit entre versiones
- `requirements.txt` — pytest 8.3 + requests

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
pytest tests/ -v
```

El mock server también corre standalone para chequeos manuales:

```bash
python mock_server.py 8571
curl -H "Authorization: Bearer test" -H "API-Version: 2025-01" http://127.0.0.1:8571/v1/tasks/T-301
curl -H "Authorization: Bearer test" -H "API-Version: 2024-03" -i http://127.0.0.1:8571/v1/tasks/T-301   # 410 Gone
```

La razón de la fixture: los bugs de compatibilidad entre versiones solo aparecen cuando un cliente viejo se encuentra con un contrato nuevo — el mock codifica los comportamientos de transición (`assignee_id` en dual, escrituras de cliente viejo mapeadas, enforcement del sunset) para que cada caso de la guía sea reproducible localmente sin un despliegue real de TaskFlow.
