# Laboratorio de Tests de Health Checks en Microservicios

Companion ejecutable de la [Checklist de Testing de Health Checks en Microservicios](https://qapractices.com/es/checklists/microservices-health-check-testing-checklist/) — un `HealthService` en Python (solo stdlib) que implementa el contrato liveness/readiness/circuit-breaker/shutdown del checklist, más una suite pytest que ejercita los modos de fallo.

## Ejecutar

```bash
pip install -r requirements.txt
pytest -v
```

## Qué cubre

| Test | Área del checklist |
|---|---|
| `test_liveness_ignores_dependencies` | Liveness nunca consulta deps (guardia anti bucle de reinicios) |
| `test_liveness_fails_only_when_process_dead` | Semántica de liveness |
| `test_readiness_503_on_critical_dep_down` | Dependencia crítica → 503 |
| `test_readiness_200_on_noncritical_dep_down` | Dependencia no crítica → sigue listo |
| `test_readiness_logs_every_probe` | Observabilidad de sondas |
| `test_breaker_opens_after_threshold` | El circuito se abre tras N fallos |
| `test_open_breaker_short_circuits_calls` | El circuito abierto bloquea llamadas |
| `test_half_open_closes_on_success` | Recuperación half-open |
| `test_open_critical_breaker_degrades_readiness` | El estado del breaker alimenta readiness |
| `test_sigterm_flips_readiness_but_not_liveness` | Contrato de graceful shutdown |
| `test_inflight_drains_before_exit` | Drenaje de peticiones en vuelo |
| `test_shutdown_does_not_outlive_grace` | Kill duro en el deadline |
| `test_aggregate_*` | Agregación de salud en el gateway |
