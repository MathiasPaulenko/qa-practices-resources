# Testing CRUD de Panel Admin — Companion

Recurso companion de [Casos de Prueba CRUD de Panel Admin: Ejemplo TaskFlow](https://qapractices.com/es/test-cases/admin-dashboard-crud-test-cases/).

## Contenido

- `mock_server.py` — API admin TaskFlow solo stdlib (`/api/v1/projects`, `/users`, `/tasks`) con auth (tokens Bearer admin/viewer), enforcement CSRF, bloqueo optimista vía `version`, soft delete con vista `include_deleted`, bulk delete con reporte de fallos parciales, paginación/búsqueda, y un log de auditoría completo en `/api/v1/audit-log`.
- `tests/conftest.py` — levanta el mock en un puerto efímero por test.
- `tests/test_admin_crud.py` — subconjunto ejecutable de los 15 casos más los edge cases: integridad referencial al borrar, visibilidad de soft-delete, conflictos de versión, validación de enum, rechazo CSRF, denegación del rol viewer y completitud del log de auditoría.
- `fixtures/` — los payloads usados por los ejemplos curl del artículo (`project-create.json`, `user-create.json`, `task-update.json`).

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
cd resources/test-cases/web-testing/admin-dashboard-crud-test-cases
pytest tests/ -v
```

Ejecuta el mock standalone para pruebas manuales:

```bash
python mock_server.py 8080

curl -X POST http://127.0.0.1:8080/api/v1/projects \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "X-CSRF-Token: csrf-token-123" \
  -H "Content-Type: application/json" \
  -d @fixtures/project-create.json
```

## Qué cubre

- CRUD crear/leer/actualizar/eliminar sobre proyectos, usuarios y tareas (camino API de TC001–TC015).
- Bloqueo optimista: `version` desfasada → `409` conflict.
- Soft delete: los registros salen de las listas por defecto, visibles con `include_deleted=true`.
- Bulk delete con reporte de fallos por registro.
- Límite de auth: el token viewer lee pero recibe `403` al escribir; sin CSRF → `403`.
- Log de auditoría: cada mutación registrada con identidad del admin, marca de tiempo, entidad y campos modificados.
