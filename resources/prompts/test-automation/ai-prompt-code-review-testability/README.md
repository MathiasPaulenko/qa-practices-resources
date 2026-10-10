# AI Prompt: Code Review Focused on Testability — Companion

Companion files for the [AI Prompt: Code Review Focused on Testability](https://qapractices.com/prompts/ai-prompt-code-review-testability) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full testability-review prompt, ready to copy-paste into any LLM. |
| `example-input.txt` | Example input: a legacy `OrderService.ts` with an inline Stripe client, a static `db` import, ambient time and swallowed errors. |
| `example-output.csv` | The findings table as importable CSV: pattern, why it blocks testing, minimal refactor, test it unlocks, severity. |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Replace the bracketed placeholders with your code, stack, test framework, coverage and refactor budget.
3. Run it on one file or diff at a time — pasting a whole service layer returns generic advice.
4. Compare the output with `example-output.csv` to sanity-check the expected format and severity scale.
5. Re-run after each landed refactor: the second pass surfaces seams the first one masked.

## Requirements

- Any LLM with room for the prompt plus a few hundred lines of code (GPT-4-class models, Claude, Copilot Chat).
- Optional: a spreadsheet or tracker that imports CSV if you want to keep the findings under version control.

## Notes

- The prompt asks for the smallest seam (Feathers' sense) — treat severity as the order that unblocks tests fastest, not a bug ranking.
- Agree on each injection point with the team before changing signatures.
- Never paste real credentials, PII or production data into the prompt.
- The related resource keeps the same content in Spanish at [qapractices.com/es](https://qapractices.com/es/prompts/ai-prompt-code-review-testability).
