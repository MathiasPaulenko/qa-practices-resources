# Checklist de Ejecución de Tests en Paralelo — Companion

Artefactos ejecutables para la [Checklist de Ejecución de Tests en Paralelo](https://qapractices.com/es/checklists/parallel-test-execution-checklist/) de QAPractices.com.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `pytest_parallel.ini` | Config de pytest-xdist: 4 workers, distribución `loadgroup`, reportes JUnit por worker, orden con seed fija. |
| `github_actions_sharding.yml` | Workflow de GitHub Actions: sharding determinista de Playwright en 4 vías más un job de merge que produce un único reporte HTML. |
| `worker_isolation.py` | Helpers de pytest que dan a cada worker de xdist su propio esquema de base de datos, rango de puertos y namespace de usuarios de test. |

## Inicio rápido

```bash
# 1. pytest-xdist en una máquina
pip install pytest-xdist
pytest -c pytest_parallel.ini tests/

# 2. Sharding entre máquinas de CI
#    copia github_actions_sharding.yml a .github/workflows/e2e-sharded.yml

# 3. Recursos por worker en tu conftest.py
from worker_isolation import worker_schema, worker_db_url
```

## La regla que importa

Aísla antes de escalar. Workers que comparten base de datos, rango de puertos o pool de usuarios de test van a competir entre sí — y los fallos se ven exactamente igual que tests flaky.
