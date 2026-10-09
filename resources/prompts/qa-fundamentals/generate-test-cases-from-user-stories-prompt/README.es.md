# Prompt de IA: Casos de Prueba desde User Stories — Companion

Archivos companion del recurso [Prompt de IA: Casos de Prueba desde User Stories](https://qapractices.com/es/prompts/generate-test-cases-from-user-stories-prompt).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | La plantilla de prompt completa lista para copiar y pegar en cualquier LLM. |
| `example-input.txt` | Ejemplo de entrada: una user story de código de descuento con criterios de aceptación y contexto. |
| `example-output.csv` | Ejemplo de salida con 8 casos de prueba en formato CSV, listo para importar a TestRail. |

## Uso

1. Copia `prompt-template.txt` en tu LLM (ChatGPT, Claude, asistentes tipo Copilot).
2. Reemplaza los placeholders entre corchetes con tu user story, criterios de aceptación y contexto.
3. Ejecuta el prompt y revisa la suite generada —verifica que cada caso mapea a un criterio de aceptación.
4. Usa `example-output.csv` como formato de referencia para importar a TestRail, Zephyr o Jira Xray.
5. Devuelve los huecos al prompt ("añade un caso negativo por nivel de permiso") y regenera.

## Requisitos

- Cualquier LLM (ChatGPT, Claude, GitHub Copilot o un modelo local).
- Opcional: una herramienta de gestión de pruebas que importe CSV o JSON (TestRail, Zephyr, Jira Xray).

## Notas

- Revisa siempre los casos generados por IA contra la aplicación real —el modelo puede inventar campos o elementos de UI que no existen.
- Una user story por ejecución; la calidad baja cuando combinas varias historias en un solo prompt.
- Trata el Risk Analysis generado como una primera opinión, no como un veredicto —corrígelo contra tu historial de defectos.
