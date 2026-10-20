# Selección de Suite de Regresión — Scorer Companion

Companion del recurso de QAPractices
[Plantilla de Selección de Suite de Pruebas de Regresión](https://qapractices.com/es/templates/regression-test-suite-selection-template/).

`regression_selector.py` implementa el modelo de scoring ponderado de la plantilla:

```
Score = CN*0.30 + HD*0.25 + IC*0.20 + AU*0.15 + TE*0.10
```

Cada columna `bc`, `dh`, `ci`, `au`, `et` se puntúa de 0 a 3:

| Columna | Criterio | Peso |
|---|---|---|
| `bc` | Criticidad de negocio | 30% |
| `dh` | Historial de defectos | 25% |
| `ci` | Impacto del cambio de código | 20% |
| `au` | Estado de automatización | 15% |
| `et` | Tiempo de ejecución | 10% |

El score ponderado asigna el tier:

| Score | Tier |
|---|---|
| 2.50 – 3.00 | T0 Smoke |
| 2.00 – 2.49 | T1 Core |
| 1.50 – 1.99 | T2 Completo |
| 0.00 – 1.49 | T3 Específico del cambio |

## Uso

```bash
pip install -r requirements.txt
python regression_selector.py test_cases.csv selection_plan.csv
```

Salida:

```text
T0:2 T1:3 T2:3 T3:2  (10 total)
```

`selection_plan.csv` lista cada prueba ordenada por score ponderado con su tier.
`test_cases.csv` replica los números del Ejemplo Completado de la plantilla.

## Tests

```bash
pytest -v
```
