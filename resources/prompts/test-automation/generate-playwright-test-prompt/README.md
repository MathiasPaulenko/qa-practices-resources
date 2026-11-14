# AI Prompt: Generate Playwright E2E Tests — Companion

Companion files for [Generate Playwright E2E Tests](https://qapractices.com/prompts/generate-playwright-test-prompt).

## Files

- `prompt-template.txt` — the full prompt, ready to paste into any LLM. Replace `[PASTE_USER_STORY_OR_ACCEPTANCE_CRITERIA]`, `[BASE_URL]` and the `[feature-name]` placeholders.
- `example-input.txt` — a filled example: saved-card checkout user story with acceptance criteria against a staging URL.
- `example-output.md` — a fragment of what the prompt returns: the `checkout.spec.ts` spec with page-object usage, fixtures, auto-retrying assertions and the empty-cart negative case.

## Usage

1. Copy `prompt-template.txt` into your LLM of choice.
2. Paste your user story or acceptance criteria where indicated.
3. Review the generated suite — fix any assertions the model composes incorrectly (e.g. `.toBeVisible().then(...)` should be two separate awaited expects).
4. Add the files to your `tests/` tree and run `npx playwright test`.

Requires Playwright 1.49+.
