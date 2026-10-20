# Laboratorio del Ciclo de Vida del Toast

Companion ejecutable de [Casos de Prueba de Notificaciones Toast: 30 Escenarios de Auto-descarte](https://qapractices.com/es/test-cases/toast-notification-auto-dismiss-test-cases/) — una máquina de estados en Python solo-stdlib que refleja el contrato del toast (montaje, cuenta regresiva, pausa en hover, tope de apilado, cola, dedup, desplazamiento por prioridad, salidas manual y por acción) más una suite pytest que ejercita los modos de fallo del recurso.

## Ejecutar

```bash
pip install -r requirements.txt
pytest -v
```

## Qué cubre

| Test | Caso de la suite |
|---|---|
| `test_auto_dismiss_fires_at_deadline` / `test_toast_visible_before_deadline` | TC-001 montaje → auto-descarte en la duración |
| `test_pause_freezes_countdown` / `test_resume_continues_from_remaining` | TC-004 pausa en hover reanuda desde el restante |
| `test_manual_close_cancels_timer` | TC-005 la X cancela el temporizador pendiente |
| `test_action_callback_fires_once` / `test_action_count_starts_at_zero` | TC-006 la acción se dispara exactamente una vez |
| `test_dead_click_after_dismiss_does_nothing` | Tabla de límites — clic en/después del borde de descarte |
| `test_dismissed_toast_is_fully_removed` | TC-010 eliminación, no solo ocultamiento |
| `test_persistent_toast_never_auto_dismisses` | TC-011 contrato de `duration: 0` |
| `test_timer_drift_within_tolerance` | TC-012 ventana de ±200ms |
| `test_stack_never_exceeds_max` | TC-013 invariante de máximo-visible en ráfaga |
| `test_queue_drains_fifo` / `test_dequeue_only_on_vacancy` | TC-024 semántica de cola secuencial |
| `test_dedup_resets_timer` | TC-017 mensaje idéntico reinicia el temporizador |
| `test_priority_preempts_lowest` / `test_low_priority_queues_when_full` | TC-025 reglas de prioridad con pila llena |
| `test_paused_toast_does_not_expire` | Borde de pausa en hover/foco |
| `test_no_duplicates_from_retry_burst` | TC-030 absorción de tormenta |
| `test_multiple_dismissals_safe` | Cierre idempotente (higiene de doble-descarte) |

## Estructura

- `toast_lifecycle.py` — `ToastManager`/`Toast`/`State` (~100 líneas, solo stdlib).
- `tests/test_toast_lifecycle.py` — 20 tests mapeados a los números TC del recurso.
