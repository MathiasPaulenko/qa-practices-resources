# Calculadora ROI de Automatización — Companion

Versión ejecutable de la [plantilla de calculadora ROI](https://qapractices.com/es/templates/test-automation-roi-calculator-template/): un script en Python sin dependencias más un CSV que replica las Secciones 1–2 de la plantilla.

## Archivos

- `roi_calculator.py` — calcula ahorros proyectados, métricas de ROI y la tabla de sensibilidad ±20%.
- `inputs.csv` — el ejemplo resuelto de e-commerce (500 casos, 80% automatizado, 2 corridas/release). Editá los valores y re-ejecutá para modelar tu propia suite.

## Uso

```bash
python roi_calculator.py            # corre el ejemplo resuelto
python roi_calculator.py inputs.csv # corre tus propios números
```

Salida esperada del ejemplo: USD 128.000 de costo manual eliminado, USD 176.000 de ahorro bruto, USD 159.500 neto, payback de 2,7 meses, ROI del primer año 343%.

## Notas

- La ejecución automatizada no tiene línea de mano de obra — las corridas de CI son tiempo de máquina. Si pagás por minuto de runner, extendé `Inputs` con un costo de ejecución.
- El mantenimiento se modela como horas anuales de ingeniero (15–25% del esfuerzo inicial es un rango razonable).
