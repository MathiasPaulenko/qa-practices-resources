# Prompt de IA: Dashboard Ejecutivo de Métricas QA — Companion

Archivos companion del recurso [Prompt de IA: Dashboard Ejecutivo de Métricas QA](https://qapractices.com/es/prompts/ai-prompt-qa-metrics-dashboard).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de diseño de dashboard, listo para copiar en un LLM. |
| `example-input.txt` | Un contexto rellenado: MedTrack, equipo QA de 12 personas, Jira + TestRail + GitHub Actions + Grafana. |
| `example-output.md` | Un fragmento de salida realista: dos tarjetas de métrica (tasa de escapes, ratio de flaky) con fórmulas, umbrales, escenarios de trampa y salvaguardas, más el flujo del lunes. |

## Uso

1. Copia `prompt-template.txt` en tu LLM.
2. Rellena el bloque de contexto con tu producto, fuentes de datos, versiones de tooling y — lo más importante — la única decisión semanal que el dashboard debe cambiar.
3. Compara la forma de la respuesta con `example-output.md`; cada métrica debe llevar fórmula, umbral, escenario de trampa y salvaguarda.
4. Lanza el checklist anti-trampa junto con el dashboard, no después.
5. Re-ejecuta cada trimestre para recalibrar umbrales contra tu propia línea base.
