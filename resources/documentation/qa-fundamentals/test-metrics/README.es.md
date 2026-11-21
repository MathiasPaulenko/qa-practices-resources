# Métricas de Prueba: Referencia Rápida — Companion

Snippets ejecutables de la guía [Métricas de Prueba: Referencia Rápida de KPIs](https://qapractices.com/es/documentation/test-metrics/) de QAPractices.

## Contenido

- `jest.config.js` — gate de cobertura para Jest 30: CI falla si la cobertura de ramas cae por debajo de 70% o la de líneas/funciones/sentencias por debajo de 80%.
- `scripts/defect_density.js` — ordena módulos por defectos por KLOC para encontrar primero el hotspot que conviene investigar. Ejecutar con `node scripts/defect_density.js`.
- `scripts/flaky_test_check.sh` — corre un spec de Jest 10 veces y cuenta los fallos, para cuantificar la inestabilidad en vez de adivinarla. Ejecutar con `./scripts/flaky_test_check.sh <ruta-al-spec>`.

## Requisitos

- Node.js 20+ con Jest 30 instalado en tu proyecto (`npm i -D jest`).
- Bash para el script de flake check (Git Bash funciona en Windows).
