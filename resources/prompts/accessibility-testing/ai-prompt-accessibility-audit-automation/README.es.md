# Prompt de IA: Automatizar Pruebas de Accesibilidad WCAG — Companion

Archivos companion del recurso [Prompt de IA: Automatizar Pruebas de Accesibilidad WCAG](https://qapractices.com/es/prompts/ai-prompt-accessibility-audit-automation).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de automatización de accesibilidad, listo para copiar y pegar en cualquier LLM. |
| `example-input.txt` | Entrada de ejemplo: el escenario de PulseCare Patient Portal (Angular 17.3, WCAG 2.2 AA, ADA Título III). |
| `example-output.md` | Fragmentos de la salida esperada: el paso del workflow de CI `a11y.yml` y un test de Playwright de indicadores de foco. |

## Uso

1. Copiá `prompt-template.txt` en tu LLM (ChatGPT, Claude, asistentes tipo Copilot).
2. Reemplazá cada placeholder entre corchetes con tu versión de framework, URL base, matriz de lectores de pantalla y alcance reales.
3. Corrélo una vez y compará la forma de la salida con `example-output.md` — si el modelo salta entregables, pedile de nuevo el ítem numerado que falta.
4. Ejecutá la suite generada en local antes de conectar el workflow al CI; las primeras corridas siempre exponen huecos del entorno.
5. Revisá cada regla de axe deshabilitada en la config generada — todas deberían llevar un comentario que las justifique.

## Requisitos

- Cualquier LLM que acepte un prompt de ~2k tokens (modelos clase GPT-4, Claude, Copilot Chat).
- Para ejecutar los tests generados: Node 20+, Playwright y una URL de staging accesible.

## Notas

- Los checks automatizados de axe detectan cerca de un tercio de los problemas WCAG — conservá los guiones manuales con lector de pantalla que genera el prompt; no son extras opcionales.
- Nunca apuntes la suite generada a producción; usá staging.
- No pegues datos reales de usuarios ni credenciales en el prompt.
