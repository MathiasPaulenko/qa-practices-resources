# Plantilla de Reglas de Validación de Calidad de Datos — Companion Ejecutable

Companion de la [Plantilla de Reglas de Validación de Calidad de Datos](https://qapractices.com/es/templates/data-quality-validation-rules-template/) / [English version](https://qapractices.com/templates/data-quality-validation-rules-template/).

`dq_runner.py` ejecuta los ocho tipos de checks del registro — completitud, unicidad, formato, rango, integridad referencial, consistencia, reglas de negocio — sobre un dataset SQLite en memoria, además de un gate de carga de filas mínimas y un score DQ ponderado. `seed(clean=False)` carga un dataset con un defecto por tipo de check para que se vea cada regla dispararse; `seed(clean=True)` produce la línea base en verde.

## Ejecución

```bash
python dq_runner.py      # imprime PASS/WARN/FAIL por check + scores por dimensión
python -m unittest discover tests -v
```

Requisitos: Python 3.9+, solo biblioteca estándar.

## Mapeo de cada check

| Check del runner | Sección de la plantilla |
|---|---|
| `check_min_rows` | 1.3 conteo de registros / gate de carga cero filas |
| `check_completeness` | 1.2 checks de nulos y valores faltantes |
| `check_uniqueness` | 2.1-2.2 duplicados de PK y clave natural |
| `check_format` | 3.1-3.3 patrones, tipos, enums |
| `check_range` | 4.1-4.3 límites numéricos y de fecha |
| `check_referential` | 5.1-5.2 huérfanos de FK |
| `check_consistency` | 6.1 reglas entre campos (pagado vs importe pagado) |
| `check_business_rules` | 7.1 reglas personalizadas (formulario aduanas, motivo cancelación) |
| `run_all` score | 7.3 score DQ ponderado |

La ejecución con el dataset sembrado reporta un score global de 25.0 con fallos en todas las dimensiones — es a propósito: el objetivo del ejemplo es ver dispararse cada check, no parecer sano.
