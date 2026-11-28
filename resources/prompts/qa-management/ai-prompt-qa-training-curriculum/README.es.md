# Prompt de IA: Generar un Plan de Formación QA — Companion

Archivos companion del recurso [Prompt de IA: Generar un Plan de Formación QA](https://qapractices.com/es/prompts/ai-prompt-qa-training-curriculum).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de diseño de plan de formación, listo para copiar en un LLM. |
| `example-input.txt` | Un contexto rellenado: 3 juniors + 1 mid QA, checkout e-commerce, Playwright + GitHub Actions, hueco de tests de API. |
| `example-output.md` | Un fragmento de salida realista: Módulo 2 con objetivos, tres laboratorios sobre el stack real, evaluación en CI y un punto de control con camino de fallo. |

## Uso

1. Copia `prompt-template.txt` en tu LLM.
2. Rellena el bloque de contexto — nombra herramientas y versiones exactas, y formula el hueco en términos de comportamiento ("nadie escribe tests de API", no "mejorar automatización").
3. Compara la forma de la respuesta con `example-output.md`; cada módulo debe traer objetivos, laboratorios sobre *tu* stack y un punto de control con camino de fallo.
4. Rechaza módulos que no sirvan al hueco — el prompt está instruido para descartarlos.
5. Re-ejecuta cuando el hueco se cierre o cambie el stack.
