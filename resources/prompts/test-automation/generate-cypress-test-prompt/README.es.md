# Prompt de IA: Generar Tests E2E con Cypress

Assets complementarios del [recurso de QAPractices](https://qapractices.com/es/prompts/generate-cypress-test-prompt/).

## Contenido

| Archivo | Propósito |
|---|---|
| `prompt-template.txt` | El prompt completo en texto plano — copialo, completá los `[placeholders]` y pegalo en tu LLM. |
| `example-input.txt` | Una entrada de ejemplo: historia de checkout sobre un entorno de staging. |
| `example-output.md` | Lo que devuelve el LLM — árbol de archivos, mapa `selectors.js`, spec `checkout.cy.js` (camino feliz + casos negativos) y fixture `users.json`. |

## Uso

1. Abrí `prompt-template.txt` y reemplazá los placeholders: historia de usuario, `URL_BASE`, método de auth, estrategia de selectores.
2. Corrélo en el LLM que uses.
3. Compará la salida con `example-output.md`; ajustá las restricciones (versión, selectores, superficie de API) y re-correlo si la suite deriva.

Mantené los specs deterministas: exigí alias de `cy.intercept` en vez de waits fijos, y solo datos sintéticos (`testmail.dev`, nunca PII real).
