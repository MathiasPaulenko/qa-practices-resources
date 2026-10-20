# Procesamiento por Lotes y Cola de Jobs — Lab Companion

Companion del recurso de QAPractices
[Casos de Prueba de Procesamiento por Lotes y Colas](https://qapractices.com/es/test-cases/batch-processing-job-queue-test-cases/).

`job_queue.py` es una cola de jobs en memoria sin dependencias que modela el
ciclo de vida que cubren los casos de prueba:

```text
queued → processing → completed
                    ↘ retrying → processing (backoff) → dead_lettered
                    ↘ cancelled / failed
dead_lettered → queued (replay tras corregir la causa)
```

- `submit()` valida payloads, rechaza tipos desconocidos y deduplica por
  `idempotency_key`.
- `run()` sigue el bucle de reintentos hasta un estado terminal.
- `replay_dlq()` reencola un job dead-lettered tras corregir la causa raíz.
- `crash_mid_job()` simula un worker que muere con el lock tomado —
  el camino del visibility timeout.

## Uso

```bash
pip install -r requirements.txt
pytest -v
```

La suite ejercita TC-001 (job individual), TC-002 (FIFO), TC-004 (reintento
transitorio), TC-008/TC-019 (máximo de reintentos → DLQ), TC-012
(idempotencia), TC-016/17 (validación de payload), TC-018/TC-026 (reencolado
tras crash), TC-028 (permanente vs transitorio) y TC-037 (replay desde DLQ).
