# AI Prompt: OAuth 2.0 and SSO Testing Scenarios

Prompt template for generating OAuth 2.0 / OIDC / SSO test scenarios: authorization code and other grant flows, token lifecycle (issuance, rotation, revocation), SSO provider integration, session management, and attack vectors such as code interception, token replay, and JWT algorithm confusion.

## Files

- `prompt-template.txt` — the prompt with placeholders for system info, SSO config, token config, and security config.
- `example-input.txt` — a filled-in example: SPA + API client with Google/Microsoft/GitHub SSO, JWT access tokens and rotating refresh tokens.
- `example-output.txt` — five representative `OAUTH-XXX` scenarios (PKCE happy path, state CSRF, refresh rotation, account-link conflict, global logout).

## Usage

1. Copy `prompt-template.txt` into your LLM.
2. Replace the bracketed variables with your system details — see `example-input.txt` for a realistic fill.
3. Ask for the scenarios category by category; the Output Format section defines the fields.

Full article: https://qapractices.com/prompts/ai-prompt-oauth-sso-testing
