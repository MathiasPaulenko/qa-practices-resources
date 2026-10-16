# Casos de Prueba de Registro de Auditoría e Historial — Companion

Recurso companion de [Casos de Prueba de Registro de Auditoría e Historial](https://qapractices.com/es/test-cases/audit-log-activity-history-test-cases/).

## Contenido

- `audit_log.py` — log de auditoría stdlib sobre sqlite3. Tabla append-only, cada entrada embebe el SHA-256 de la anterior (hash chain), `verify_chain()` devuelve el primer índice inválido, más filtrado, export CSV, limpieza por retención y legal hold. `tamper()` es un backdoor de test que hace un UPDATE directo para simular manipulación a nivel base de datos.
- `tests/test_audit_log_cases.py` — suite pytest 8.3 mapeada a los TC del recurso: campos requeridos (TC001), scrub de contraseñas (TC003/TC019), detección de manipulación (TC018), escrituras concurrentes (TC021), preservación de usuarios eliminados (TC023), unicode (TC026), verificación de cadena (TC029), legal hold vs retención (TC033), completitud del export (TC020, escalado a 2.000 filas), filtros (TC009-011), marcado de acciones API (TC025) y forma de entrada serializable a JSON.
- `tests/conftest.py` — fixture `log`: un `AuditLog` nuevo por test, file-backed para que el pool de hilos de TC021 comparta la conexión.
- `requirements.txt` — solo pytest 8.3.4; el resto es stdlib.

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
cd resources/test-cases/security-testing/audit-log-activity-history-test-cases
pytest tests/ -v
```

Prueba manual:

```bash
python - <<'PY'
from audit_log import AuditLog
log = AuditLog(":memory:")
log.append("user.login", "U-01", "login", ip_address="192.168.1.100")
log.append("admin.export", "U-01", "export", resource="report:42")
print(log.verify_chain())          # {'chainValid': True, ...}
log.tamper(1, "user_id", "U-99")   # edición directa en DB
print(log.verify_chain())          # {'chainValid': False, 'firstInvalidIndex': 1}
PY
```

## Qué cubre

- Tamper-evidence por hash chain: `hash_n = SHA-256(hash_n-1 + campos)`; un UPDATE directo rompe la cadena en esa fila y todas las posteriores.
- Scrub de datos sensibles en la capa de logging — las claves `password`, `token`, `secret`, `api_key`, `ssn` nunca llegan al almacenamiento.
- Borde de retención y legal hold — las entradas en hold sobreviven a la purga.
- Preservación de usuarios eliminados — el borrado estilo GDPR marca `deleted_user` pero mantiene entradas y cadena intactas.
- Escrituras concurrentes vía thread pool — la cadena sigue válida.
- Filtro por usuario / acción / rango de fechas y export CSV completo sin truncamiento.

## Notas de diseño

- Los timestamps se guardan en ISO-8601 UTC; datetimes naive se convierten a UTC en `append()`.
- `filter()` usa queries parametrizadas — mismo contrato que un endpoint `/v1/logs` real.
- El companion replica a propósito la semántica de la API ficticia AuditTrail del recurso (`eventType`, `userId`, `firstInvalidIndex`) para que las expectativas de los tests se traduzcan directo.
