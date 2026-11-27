# Prompt IA: Casos de Test Negativos — Companion

Archivos complementarios del recurso [Prompt IA: Casos de Test Negativos](https://qapractices.com/es/prompts/ai-prompt-generate-negative-test-cases).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de negative testing, listo para copiar en un LLM. |
| `example-input.txt` | Un contexto realista de contrato de API: endpoint, stack, reglas de validación y restricciones. |
| `example-output.md` | Un fragmento de salida realista: 12 casos priorizados cubriendo las cinco categorías. |
| `negative-payloads.csv` | Una lista semilla de payloads exactos por categoría — usable como data source CSV para tests parametrizados. |

## Uso

1. Copiá `prompt-template.txt` en tu LLM.
2. Reemplazá los placeholders entre corchetes con tu contrato real, stack, reglas de validación y restricciones.
3. Compará la respuesta con `example-output.md`; una buena respuesta usa valores de entrada exactos, nombra el comportamiento esperado observable, prioriza por riesgo y marca los puntos ambiguos del contrato.
4. Usá `negative-payloads.csv` como data source inicial para tests parametrizados — payload, campo sugerido y sonda esperada por fila.
5. Las filas marcadas "spec muda" o ambiguas son hallazgos de contrato: arreglá el contrato de la API, no el test.

## Requisitos

- Sin herramientas; la salida es una tabla de casos.
- Los payloads con forma de inyección son fixtures de test para escribir en campos — nunca ejecutarlos contra un objetivo real.
- Un entorno de staging para ejecutar las filas con estado y de concurrencia.
