# Prompt de IA: Plan de Pruebas de App Móvil — Companion

Archivos companion del recurso [Prompt de IA: Plan de Pruebas de App Móvil](https://qapractices.com/es/prompts/ai-prompt-mobile-app-testing).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | La plantilla de prompt completa lista para copiar y pegar en cualquier LLM. |
| `example-input.txt` | Ejemplo de entrada: MedDrop, una app React Native de entrega de medicamentos con su matriz de dispositivos. |
| `example-output.csv` | Ejemplo de salida: 9 casos de prueba cubriendo biometría, push, sync offline, compatibilidad, rendimiento y Crashlytics — importable a cualquier herramienta que acepte CSV. |

## Uso

1. Copia `prompt-template.txt` en tu LLM (ChatGPT, Claude, asistentes tipo Copilot).
2. Rellena el bloque `App and Environment` con tus dispositivos, granja y proveedores reales.
3. Ejecútalo y revisa el plan —cada caso debe llevar una entrada en la columna de evidencia.
4. Usa `example-output.csv` como formato de referencia para importar a TestRail, Jira o Azure DevOps.
5. Devuelve los huecos al prompt ("añade un caso para plegable") y regenera.

## Requisitos

- Cualquier LLM (ChatGPT, Claude, GitHub Copilot o un modelo local).
- Una fuente de dispositivos reales para la ejecución: BrowserStack, Sauce Labs o un pool de dispositivos físicos.

## Notas

- Rellena la matriz con los modelos que tus analytics realmente muestran —las sesiones de granja en dispositivos sin usuarios son presupuesto tirado.
- Conserva la columna de session ID: es lo que convierte un fallo en una sesión reproducible.
- Trata los diálogos de permisos de iOS y Android como casos separados —difieren lo suficiente para importar.
