# Casos de Prueba de Eliminación de Datos GDPR — Companion

Recurso complementario de [Casos de Prueba de Eliminación de Datos GDPR](https://qapractices.com/es/test-cases/gdpr-data-deletion-testing-test-cases/).

## Contenido

- `erasure_engine.py` — modelo `sqlite3` solo-stdlib del flujo del Artículo 17. `request_erasure()` exige verificación de identidad, consulta `legal_holds` (diferimiento del Art. 17(3)) y luego propaga el borrado por `users`, `orders` (columnas identificadoras a NULL, importes conservados), `sessions`, `search_index`, `cache`, `app_logs` (limpieza de valores) y `marketing_segments`, escribiendo una entrada en `audit_log` y un mensaje de buzón por procesador. `snapshot()`/`restore()` simulan un backup previo a la supresión cuyas filas resucitadas se re-borran con `replay_tombstones()`.
- `tests/test_erasure_cases.py` — suite pytest 8.3 con 16 tests mapeados a los ids de TC del recurso: cascada (TC-002), limpieza de índice/caché (TC-003), replay tras restore (TC-004), rastro de auditoría (TC-005), notificación a procesadores (TC-006), retención legal y reanudación (TC-007), agregados anonimizados (TC-008), ventana legal de un mes (TC-009), rechazo de solicitudes no verificadas (TC-010), limpieza de logs (TC-011), resistencia a la re-identificación (TC-012), repeticiones idempotentes (TC-013), alcance de retirada de consentimiento (TC-014), contenido de la confirmación (TC-015) y la carrera con el export (TC-016).
- `tests/conftest.py` — fixture `engine`: `ErasureEngine` en memoria sembrado con `u-4821` / `qa-erasure-01@taskflow.test`.
- `requirements.txt` — solo pytest 8.3.4; el motor es stdlib puro.

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
cd resources/test-cases/security-testing/gdpr-data-deletion-testing-test-cases
pytest tests/ -v
```

Prueba manual:

```bash
python - <<'PY'
from erasure_engine import ErasureEngine
eng = ErasureEngine()
eng.seed_user("u-4821", "qa-erasure-01@taskflow.test")
print(eng.request_erasure("u-4821"))          # {'status': 'fulfilled', ...}
print(eng.pii_residue("qa-erasure-01"))       # 0 — no queda nada en ningún store
snap = eng.snapshot()
eng.seed_user("u-0001", "canary@taskflow.test")
eng.request_erasure("u-0001")
eng.restore(snap)                             # resucita u-0001, el replay lo vuelve a borrar
print(eng.pii_residue("canary"))              # 0
PY
```

## Qué cubre

- La cadena de propagación que revisan las auditorías GDPR reales: tabla principal, filas relacionadas, cachés, índices de búsqueda, logs, procesadores y rastro de auditoría.
- Seguridad de backups: un restore de datos previos a la supresión va seguido del replay de tombstones para que los usuarios borrados sigan borrados.
- Los dos bordes legales que la mayoría de suites omite: diferimiento y reanudación por retención legal (Art. 17(3)) y verificación de identidad previa (Art. 12(6)).
- Semántica de anonimización: los pedidos sobreviven como agregados, pero toda columna identificadora queda en NULL — y `reidentify()` demuestra que no hay linkage de vuelta.
- Idempotencia: una supresión repetida o de usuario inexistente es un no-op, sin notificaciones duplicadas ni spam de auditoría.

## Notas de diseño

- El motor replica el dataset TaskFlow del recurso (`u-4821`, `qa-erasure-01@taskflow.test`) para que las expectativas traduzcan directamente.
- `pii_residue(needle)` es el chequeo tipo grep de marcador canario que recomienda el recurso: una llamada barre todos los stores con PII.
- `confirmation_for()` modela el recibo al interesado: alcance y timestamp solamente — no debe contener los valores borrados.
