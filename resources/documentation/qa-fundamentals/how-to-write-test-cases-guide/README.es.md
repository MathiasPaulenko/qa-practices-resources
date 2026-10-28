# Cómo Escribir Casos de Prueba — Suite Nimbus Cart

Companion de [Cómo Escribir Casos de Prueba: de Escenarios a Pasos](https://qapractices.com/es/documentation/how-to-write-test-cases-guide/) en QAPractices.

```text
nimbus-cart-3-2-6-test-cases.csv   los 8 casos trabajados (TC-EC-02-001..005, TC-EC-03-001..003)
test-case-template.md              plantilla reutilizable con los mismos campos
```

## Importar la suite

El CSV usa un formato compatible con TestRail/Xray: `ID, Title, Scenario ID, Requirement, Priority, Tags, Preconditions, Steps, Expected Result, Actual Result, Status`. Importalo tal cual en tu TMS, o copiá filas a la plantilla cuando escribas casos nuevos.

## Cadena de trazabilidad

Cada fila mapea `REQ-EC-xx` (requerimiento) → `SC-EC-xx` (escenario) → `TC-EC-xx-NNN` (caso) — la misma cadena que la guía construye paso a paso. Sirve para ver cómo funciona en la práctica el reporte de cobertura por requerimiento.

Nimbus Cart 3.2.6 es una app ficticia de supermercado; todos los usuarios, entornos y datos son ilustrativos.
