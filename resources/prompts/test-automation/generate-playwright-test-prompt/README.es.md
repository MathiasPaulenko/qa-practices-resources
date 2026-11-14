# Prompt de IA: Generar Tests E2E con Playwright — Companion

Archivos companion para [Generar Tests E2E con Playwright](https://qapractices.com/es/prompts/generate-playwright-test-prompt).

## Archivos

- `prompt-template.txt` — el prompt completo, listo para pegar en cualquier LLM. Reemplazá `[PASTE_USER_STORY_OR_ACCEPTANCE_CRITERIA]`, `[BASE_URL]` y los placeholders `[feature-name]`.
- `example-input.txt` — un ejemplo completo: historia de usuario de checkout con tarjeta guardada y criterios de aceptación contra una URL de staging.
- `example-output.md` — un fragmento de lo que devuelve el prompt: el spec `checkout.spec.ts` con page objects, fixtures, aserciones con auto-reintento y el caso negativo de carrito vacío.

## Uso

1. Copiá `prompt-template.txt` en tu LLM preferido.
2. Pegá tu historia de usuario o criterios de aceptación donde se indica.
3. Revisá la suite generada — corregí aserciones mal compuestas (p. ej. `.toBeVisible().then(...)` deberían ser dos expects await separados).
4. Sumá los archivos a tu árbol `tests/` y corré `npx playwright test`.

Requiere Playwright 1.49+.
