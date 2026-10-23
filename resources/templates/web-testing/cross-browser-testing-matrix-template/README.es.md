# Plantilla de Matriz de Pruebas Cross-Browser — Companion

CSV listo para completar de la matriz de navegadores más un script que asigna
prioridades P1–P4 desde cuotas de tráfico reales — la misma decisión que
codifica la Sección 1.3 de la plantilla.

## Archivos

| Archivo | Qué es |
|---|---|
| `browser-matrix-template.csv` | Matriz vacía (columnas P1/P2/P3) para importar a hoja de cálculo o herramienta de gestión |
| `priority_calculator.py` | Script solo-stdlib: cuota de tráfico % → nivel de prioridad + scope de prueba recomendado |
| `traffic-sample.csv` | Export de cuotas de tráfico de muestra que lee el calculador |
| `test_priority_calculator.py` | Suite pytest cubriendo umbrales y mapeo de scopes |

## Ejecutar

```bash
python priority_calculator.py traffic-sample.csv
```

Umbrales custom si tu distribución de tráfico difiere:

```bash
python priority_calculator.py traffic-sample.csv --p1 40 --p2 10 --p3 3
```

```bash
pytest test_priority_calculator.py
```

Volver a la plantilla: https://qapractices.com/es/templates/cross-browser-testing-matrix-template/
