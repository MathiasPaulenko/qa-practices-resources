# Laboratorio de Tests de Skeleton Loading

Companion ejecutable de [Casos de Prueba de Skeleton Loading](https://qapractices.com/es/test-cases/skeleton-loading-placeholder-test-cases/) — una máquina de estados en Python (solo stdlib) que replica el ciclo de vida del skeleton (mount → tiempo mínimo de display → éxito/error/timeout, reintento, reduced-motion) más una suite pytest que ejercita los modos de fallo del recurso.

## Ejecutar

```bash
pip install -r requirements.txt
pytest -v
```

## Qué cubre

| Test | Caso de la suite |
|---|---|
| `test_skeleton_never_stays_loading` | TC-007/013/014 toda salida sale de LOADING |
| `test_min_display_time_holds` | TC-009/016 suelo anti-flash de 300ms |
| `test_slow_load_shows_natural_duration` | TC-010 carga larga |
| `test_shimmer_runs_while_loading` | TC-002 shimmer activo |
| `test_reduced_motion_disables_shimmer` | TC-022 placeholder estático conserva ARIA |
| `test_content_exit_is_single_clean_swap` | TC-013 un solo intercambio, sin doble resolve |
| `test_error_exit_sets_aria_busy_false` | TC-007 la salida de error limpia busy |
| `test_timeout_exit_is_retryable` | TC-014 timeout → reintento → LOADING |
| `test_retry_restores_shimmer_and_busy` | TC-014 semántica de reintento |
| `test_no_retry_from_content` | El éxito es terminal |
| `test_analytics_event_fires_once` | TC-028 evento de display-time |
| `test_layout_match_within_tolerance` | TC-001 bounding-box ±2px |
| `test_layout_match_rejects_drift` | TC-011 detecta deriva de geometría |
| `test_layout_match_rejects_count_mismatch` | TC-004 contrato de conteo |
| `test_aria_contract_while_loading` / `_after_exit` | TC-021 aria-busy + aria-hidden |
