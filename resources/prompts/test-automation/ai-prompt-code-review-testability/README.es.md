# Prompt de IA: Code Review Enfocado en Testabilidad — Companion

Archivos companion del recurso [Prompt de IA: Code Review Enfocado en Testabilidad](https://qapractices.com/es/prompts/ai-prompt-code-review-testability).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de revisión de testabilidad, listo para copiar y pegar en cualquier LLM. |
| `example-input.txt` | Entrada de ejemplo: un `OrderService.ts` legado con cliente Stripe en línea, import `db` estático, tiempo ambiente y errores tragados. |
| `example-output.csv` | La tabla de hallazgos como CSV importable: patrón, por qué bloquea los tests, refactor mínimo, test que desbloquea y severidad. |

## Uso

1. Copia `prompt-template.txt` en tu LLM (ChatGPT, Claude, asistentes tipo Copilot).
2. Reemplaza los corchetes con tu código, stack, framework de tests, cobertura y presupuesto de refactor.
3. Corre el prompt sobre un archivo o diff por vez — pegar una capa completa devuelve consejos genéricos.
4. Compara la salida con `example-output.csv` para validar el formato esperado y la escala de severidad.
5. Vuelve a correrlo después de cada refactor mergeado: la segunda pasada expone seams que la primera ocultaba.

## Requisitos

- Cualquier LLM con espacio para el prompt más unos cientos de líneas de código (modelos clase GPT-4, Claude, Copilot Chat).
- Opcional: una planilla o tracker que importe CSV si quieres mantener los hallazgos bajo control de versiones.

## Notas

- El prompt pide el seam más chico (en el sentido de Feathers) — leé la severidad como el orden que desbloquea tests más rápido, no como ranking de bugs.
- Acuerda cada punto de inyección con el equipo antes de cambiar firmas.
- Nunca pegues credenciales reales, PII ni datos de producción en el prompt.
