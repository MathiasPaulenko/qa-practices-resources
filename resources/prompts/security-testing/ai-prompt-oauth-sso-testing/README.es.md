# Prompt de IA: Escenarios de Testing de OAuth 2.0 y SSO

Plantilla de prompt para generar escenarios de testing de OAuth 2.0 / OIDC / SSO: grant flows, ciclo de vida de tokens (emisión, rotación, revocación), integración con proveedores SSO, gestión de sesiones y vectores de ataque como interceptación del code, replay de tokens y confusión de algoritmos JWT.

## Archivos

- `prompt-template.txt` — el prompt con placeholders para información del sistema, configuración SSO, de tokens y de seguridad.
- `example-input.txt` — ejemplo completo: cliente SPA + API con SSO de Google/Microsoft/GitHub, access tokens JWT y refresh tokens rotativos.
- `example-output.txt` — cinco escenarios representativos `OAUTH-XXX` (happy path PKCE, CSRF de state, rotación de refresh, conflicto de vinculación de cuentas, logout global).

## Uso

1. Copia `prompt-template.txt` en tu LLM.
2. Reemplaza las variables entre corchetes con los datos de tu sistema — `example-input.txt` muestra un relleno realista.
3. Pide los escenarios categoría por categoría; la sección Output Format define los campos.

Artículo completo: https://qapractices.com/es/prompts/ai-prompt-oauth-sso-testing
