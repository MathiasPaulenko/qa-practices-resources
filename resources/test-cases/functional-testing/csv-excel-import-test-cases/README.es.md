# Lab de Test de Import CSV

Companion ejecutable de [Casos de Prueba de Import CSV y Excel](https://qapractices.com/es/test-cases/csv-excel-import-test-cases/) — un importador Python solo con stdlib que ejercita los modos de fallo de la suite: sniffing de delimitador, BOM, normalización de headers, errores por fila, duplicados, import parcial vs atómico y sanitización de inyección por fórmulas.

## Correr

```bash
pip install -r requirements.txt
pytest -v
```

## Qué cubre

Cada test mapea a un caso de la suite: happy path (TC001), delimitador erróneo (TC002), BOM (TC003), errores por fila (TC005/TC006), duplicados (TC007), mapeo de headers (TC008), quoting RFC 4180 (TC009), filas vacías, rollback y parcial (TC012), inyección de fórmulas (TC013), extensión falsa (TC014) y resumen honesto (TC015).
