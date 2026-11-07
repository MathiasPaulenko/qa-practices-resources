# Plan de Pruebas de DLC — Archivos de datos

Matrices de prueba machine-readable de la [Plantilla de Plan de Pruebas de DLC](https://qapractices.com/es/templates/game-dlc-testing-plan-template/) de QAPractices.

## Archivos

| Archivo | Qué contiene |
|---|---|
| `save-compatibility-matrix.json` | 8 escenarios de save (base/DLC × instalado/no instalado, mitad de quest, cross-platform, desinstalación, rollback) con resultado esperado — las filas que atrapan la corrupción de saves. |
| `certification-requirements.json` | Categorías de chequeos de certificación por plataforma (TRC, XR, Lotcheck, Steamworks, Epic) más el fallo inicial más común de cada una. |

## Cómo usar

1. Carga `save-compatibility-matrix.json` en tu herramienta de gestión de pruebas — cada escenario tiene ID, resultado esperado y categoría.
2. Sigue la certificación con `certification-requirements.json`: marca cada chequeo por plataforma; corre el `common_first_failure` en la semana uno sobre un sandbox de la store.
3. Aplica la `sign_off_rule`: nada de aprobación mientras haya defectos de certificación Críticos/Altos abiertos sin decisión documentada.

## English

The [English version](README.md) describes the same files.
