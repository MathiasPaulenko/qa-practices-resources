# AI Prompt: Generate Cypress E2E Tests

Companion assets for the [QAPractices prompt resource](https://qapractices.com/prompts/generate-cypress-test-prompt/).

## Contents

| File | Purpose |
|---|---|
| `prompt-template.txt` | The full prompt as plain text — copy, fill the `[bracketed]` placeholders, paste into your LLM. |
| `example-input.txt` | A filled-in example: checkout user story on a staging environment. |
| `example-output.md` | What the LLM returns — file tree, `selectors.js` map, `checkout.cy.js` spec (happy path + negative cases) and a `users.json` fixture. |

## Usage

1. Open `prompt-template.txt` and replace the placeholders: user story, `BASE_URL`, auth method, selector strategy.
2. Run it against your LLM of choice.
3. Compare the output with `example-output.md`; tighten constraints (version, selector strategy, API surface) and re-run if the suite drifts.

Keep generated specs deterministic: insist on `cy.intercept` aliases over fixed waits, and synthetic test data only (`testmail.dev`, never real PII).
