# AI Prompt: Generate GraphQL Test Queries — Companion

Companion files for the [AI Prompt: Generate GraphQL Test Queries](https://qapractices.com/prompts/ai-prompt-generate-graphql-queries) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full GraphQL test-query generation prompt, ready to copy into an LLM. |
| `example-input.txt` | A small order-management SDL excerpt plus endpoint, authorization, pagination and fixture context. |
| `example-output.md` | A realistic output fragment: reusable fragment, named query and mutation, coverage matrix and review notes. |

## Usage

1. Copy `prompt-template.txt` into your LLM.
2. Replace the bracketed placeholders with your real SDL, endpoint, authorization model, runtime rules and fixture constraints.
3. Compare the response shape with `example-output.md`; if coverage areas are missing, ask for that numbered section again.
4. Validate every generated operation against your real schema before running it. Treat generated GraphQL as untrusted code.
5. Run mutations only against controlled staging fixtures and review cleanup or rollback steps first.

## Requirements

- A schema-aware GraphQL client, IDE or validation step in CI.
- Staging fixtures for any mutation or sensitive-field test.
- No real customer, payment or production data in prompts or variables.
