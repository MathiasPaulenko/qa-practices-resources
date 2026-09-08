# Checklist de Cierre de Testing — Script y Fixtures Companion

> Recurso companion de [Checklist de Cierre de Testing](https://qapractices.com/es/checklists/test-closure-checklist) en QAPractices.com.

Generador de Test Exit Report en Python, fixtures de datos de test y workflow de CI para cierre de testing con Python 3.12 y pytest 8.3.

## Requisitos

- Python 3.12+
- pytest 8.3

## Setup

```bash
# Instalar dependencias
pip install pytest==8.3

# Generar el Test Exit Report
python scripts/generate_exit_report.py --release v2.1.0 --results fixtures/test_results.json --defects fixtures/open_defects.json

# Correr los tests de validación de cierre
pytest scripts/test_closure_validation.py -v

# Correr el workflow de CI localmente
python scripts/generate_exit_report.py --release v2.1.0 --results fixtures/test_results.json --defects fixtures/open_defects.json --output reports/
```

## Archivos

| Archivo | Propósito |
| --------- | ----------- |
| `scripts/generate_exit_report.py` | Script de Python para generar un Test Exit Report a partir de resultados de test y defectos abiertos |
| `scripts/test_closure_validation.py` | Tests de pytest para validar ítems de la checklist de cierre (cobertura, defectos, artefactos) |
| `fixtures/test_results.json` | Resultados de test de ejemplo con estados passed, failed y blocked |
| `fixtures/open_defects.json` | Defectos abiertos de ejemplo con severidad, owner e impacto de negocio |
| `.github/workflows/closure-validation.yml` | Workflow de CI para validar el cierre en cada push a rama de release |

## Datos de Test

El directorio `fixtures/` contiene datos de test reutilizables:

- `test_results.json` — 20 test cases con estados mixtos (passed, failed, blocked)
- `open_defects.json` — 5 defectos abiertos con niveles de severidad e impacto de negocio

## Licencia

MIT — libre de usar, modificar y distribuir. Nunca guardes credenciales de producción en fixtures de test; siempre usá datos sintéticos.
