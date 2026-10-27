# Risk-Based Testing — Recursos Complementarios

Artefactos iguales a los ejemplos de [Risk-Based Testing: Enfoque Práctico](https://qapractices.com/es/documentation/risk-based-testing/).

## Contenido

| Archivo | Propósito |
|---|---|
| `src/risk-register.csv` | Plantilla de registro de riesgos: área, probabilidad (1-5), impacto (1-5), score, prioridad, tests de mitigación, responsable. Precargada con el ejemplo de e-commerce de la guía. |
| `src/pytest.ini` | Registro de markers `critical`, `high`, `medium`, `low` para que el filtrado con `pytest -m` funcione sin warnings. |
| `src/test_risk_markers.py` | Tests de ejemplo etiquetados con markers de riesgo, iguales al pipeline de CI de la guía. |
| `src/risk-report-template.md` | Tabla de resumen de tests por nivel de riesgo + bloque de riesgos abiertos, lista para pegar en un reporte de release. |

## Uso

```bash
# Correr solo tests de riesgo crítico y alto
pytest -m "critical or high"

# Pasada profunda de riesgo antes del release
pytest -m "critical" --count 3   # requiere pytest-repeat
```

Convención de scoring: `Nivel de Riesgo = Probabilidad x Impacto`, ambos en escala 1-5. Scores de 15+ mapean a Crítico, 8-14 Alto, 4-7 Medio, menos de 4 Bajo — ajustá los umbrales a tu contexto.
