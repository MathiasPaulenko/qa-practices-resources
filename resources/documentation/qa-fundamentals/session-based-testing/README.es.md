# Companion de Pruebas Basadas en Sesiones

Recurso companion de la [Guía de Pruebas Basadas en Sesiones](https://qapractices.com/es/documentation/session-based-testing). Contiene las plantillas de trabajo para aplicar SBTM sin preparación: plantilla de charter, plantilla de reporte de sesión y tracker de métricas.

## Archivos

| Archivo | Propósito |
| ------- | --------- |
| `src/charter-template.md` | Esqueleto de charter con la estructura qué/cómo/por qué y pistas de tamaño. Copia uno por sesión. |
| `src/session-report-template.md` | Formato completo de reporte: entorno, notas cronológicas, bugs, issues y checklist de cobertura. |
| `src/session-metrics.csv` | Tracker de métricas: sesiones por día, completitud de charters, tasa de hallazgo de bugs, ratio de setup y ratio test/investigación — con metas y umbrales de bandera roja de la guía. |

## Inicio rápido

1. Escribe un charter por sesión desde `charter-template.md` — rellena las tres líneas y estima 60-90% de una sesión de 90 minutos.
2. Durante la sesión, toma notas cronológicas directamente en una copia de `session-report-template.md`.
3. En las siguientes 24 horas, haz el debrief (PROOF: Past, Results, Obstacles, Outlook, Feelings).
4. Registra la sesión en `session-metrics.csv` y revisa los umbrales de bandera roja cada semana.

## Requisitos

Ninguno. Las plantillas markdown abren en cualquier editor; el CSV importa a Excel, Google Sheets o tu wiki.
