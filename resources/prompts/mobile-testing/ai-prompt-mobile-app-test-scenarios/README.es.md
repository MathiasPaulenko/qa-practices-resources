# Prompt de IA: Escenarios de Testing de Aplicaciones Móviles — Companion

Archivos complementarios del recurso [Prompt de IA: Escenarios de Testing de Aplicaciones Móviles](https://qapractices.com/es/prompts/ai-prompt-mobile-app-test-scenarios).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | La plantilla completa del prompt, lista para copiar y pegar en cualquier LLM. |
| `example-input.txt` | Entrada de ejemplo: FitPulse, una app de fitness en React Native con su contexto de dispositivos y red. |
| `example-output.csv` | Salida de ejemplo: 12 escenarios de ciclo de vida, offline, biometría, push, interrupciones, fragmentación, permisos de salud y cross-platform — importable a cualquier herramienta de gestión de pruebas con CSV. |

## Uso

1. Copia `prompt-template.txt` en tu LLM (ChatGPT, Claude, Copilot u otro asistente).
2. Reemplaza los placeholders entre corchetes de los bloques `App Under Test` y `Device and Environment Constraints` con el contexto real de tu app.
3. Ejecuta y revisa el indicador de falla de cada escenario — ese campo es lo que convierte una fila en un reporte de bug listo para triage.
4. Usa `example-output.csv` como formato de referencia para importar a TestRail, Jira o Azure DevOps.
5. Vuelve a ejecutar por plataforma cuando las diferencias iOS/Android importen (entrega de push, diálogos de permisos, límites en background).

## Requisitos

- Cualquier LLM (ChatGPT, Claude, GitHub Copilot o un modelo local).
- Para la ejecución: dispositivos reales o una granja (BrowserStack, Sauce Labs) más la herramienta que sugiere cada escenario (Appium, XCUITest, Espresso, Detox, Maestro).

## Notas

- Llena la lista de dispositivos con los modelos que realmente muestran tus analíticas — las listas genéricas producen escenarios genéricos.
- Mantén al menos un edge case por categoría; las filas de interrupciones y ciclo de vida son donde viven los crashes reales.
- Revisa la salida con un QA senior antes de que llegue al repositorio de pruebas: los LLM aún pasan por alto particularidades de plataforma como las restricciones de alarmas exactas de Android.
