# Casos de Prueba de Release Testing: suite de smoke-gate ejecutable

Companion de la guía de QAPractices [Casos de Prueba de Release Testing: Smoke y Regresión](https://qapractices.com/es/test-cases/release-testing-test-cases/).

Una mini-app Flask que simula un servicio desplegado — `/health` con sondas de dependencias, metadata de entorno, checksums de artefacto, feature flags y un endpoint de rollback — más una suite pytest 8.3 que implementa las partes automatizables de la guía: RT-SM-03/04, RT-ENV-01/04 y los casos límite específicos del release.

## Estructura del proyecto

```text
├── app.py                          # App Flask: health, metadata de entorno, flags, rollback
├── tests/test_release_smoke.py     # Suite pytest: smoke + entorno + casos límite
├── .github/workflows/release-gate.yml  # Ejemplo de gate post-despliegue (deployment_status)
└── requirements.txt
```

## Mapeo de conceptos

| Caso de prueba | Qué demuestra | Función |
|---|---|---|
| RT-SM-03 | `/health` responde 200 en menos de 500 ms | `test_health_endpoint_200_and_fast` |
| RT-SM-03/04 | Cada dependencia reporta `up`; degrada cuando una falla | `test_health_*`, `test_health_degrades_when_a_dependency_is_down` |
| RT-ENV-01 | La suite rechaza un objetivo que no es producción | `test_environment_*` |
| RT-ENV-04 | Sin migraciones pendientes en el release | `test_no_pending_migrations`, `test_pending_migrations_are_detected` |
| Límite: checksum | El hash del artefacto desplegado debe igualar al del build | `test_artifact_checksum_*`, `test_checksum_mismatch_is_detected` |
| Límite: ventana de rollback | Rollback permitido dentro de la ventana, rechazado (409) fuera | `test_rollback_*` |

## Requisitos

- Python 3.10+, `pip install -r requirements.txt` (Flask 3.x, pytest 8.3).

## Uso

```bash
pip install -r requirements.txt
pytest -v
```

No hace falta levantar servidor — los tests usan el test client de Flask. Para probar la app a mano:

```bash
python app.py            # sirve en :5000
curl http://localhost:5000/health
curl http://localhost:5000/meta/environment
```

Simula modos de fallo con variables de entorno — por ejemplo `CACHE_UP=0`, `PENDING_MIGRATIONS=2`, `APP_ENV=staging`, `ARTIFACT_SHA=deadbee`, o un `DEPLOY_STARTED_AT` más viejo que la ventana de rollback de 30 minutos.

Contra un despliegue real, los mismos tests corren sobre una URL viva en lugar del test client — la guía muestra la variante con `requests` y el gate de GitHub Actions con `deployment_status` (`release-gate.yml`).

## Notas

- El artículo y esta suite se versionan juntos: pytest 8.3, requests 2.32, Flask 3.x.
