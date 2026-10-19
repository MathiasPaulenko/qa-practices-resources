# Laboratorio de Tests de Rollout de Feature Flags

Companion ejecutable de [Casos de Prueba de Feature Flags](https://qapractices.com/es/test-cases/feature-flag-rollout-test-cases/) — un evaluador de flags en Python (solo stdlib) que replica el orden de evaluación estilo OpenFeature (existe → habilitado → prerequisitos → regla de usuario → regla de segmento → bucket porcentual) más una suite pytest que ejercita los modos de fallo de rollout determinista del recurso.

## Ejecutar

```bash
pip install -r requirements.txt
pytest -v
```

## Qué cubre

| Test | Caso de la suite |
|---|---|
| `test_rollout_is_deterministic` | TC-004 mismo usuario, mismo resultado |
| `test_rollout_distribution_is_plausible` | TC-004 banda ~50% |
| `test_zero_and_hundred_percent_boundaries` | TC-005 límites del rollout |
| `test_user_targeting_hits_and_misses` | TC-006 listas de usuarios |
| `test_segment_targeting` | TC-007 membresía de segmento |
| `test_rollout_increase_is_monotonic` | TC-010 nadie pierde acceso |
| `test_missing_flag_returns_default` | TC-011 default sin crash |
| `test_anonymous_user_gets_default` | TC-012 sin contexto de usuario |
| `test_bucket_boundary_is_exclusive` | TC-013 bucket == porcentaje |
| `test_user_deny_beats_segment_allow` | TC-014 precedencia de reglas |
| `test_prerequisite_unmet_blocks_child` | TC-016 dependencia bloqueante |
| `test_prerequisite_met_lets_child_evaluate` | TC-017 dependencia cumplida |
| `test_rapid_toggling_last_write_wins` | TC-018 orden de toggles |
| `test_ab_variant_is_stable` / `test_ab_variants_distribute` | TC-023 asignación de variante |
| `test_flag_evaluation_latency` | Presupuesto de latencia (1000 evals < 100 ms) |

## Encontrar un usuario en el límite (TC-013)

```bash
python tests/find_bucket.py new-dashboard 50
```

Imprime el primer `user-NNNNN` cuyo bucket sha256 es exactamente 50 — el usuario que evalúas al 50% vs 51% para verificar la regla inclusiva/exclusiva.
