# AI Prompt: Mobile Interruption Tests — Companion

Companion files for the [AI Prompt: Mobile Interruption Tests](https://qapractices.com/prompts/ai-prompt-generate-interruption-tests) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full mobile interruption-test generation prompt, ready to copy into an LLM. |
| `example-input.txt` | A realistic checkout context with Android/iOS versions, authentication, triggers, backend recovery behavior and staging constraints. |
| `example-output.md` | A realistic output fragment: interruption matrix and detailed cases for calls, network loss, process death, lock/unlock and notifications. |

## Usage

1. Copy `prompt-template.txt` into your LLM.
2. Replace the bracketed placeholders with your real app context, lifecycle constraints, backend recovery contract and available devices.
3. Compare the response with `example-output.md`; every high-risk case should include recovery assertions, backend or state checks, cleanup and automation feasibility.
4. Review platform assumptions manually before executing. Android and iOS interruption behavior is related, not identical.
5. Run transactional cases only in staging with controlled fixtures. Never use real phone numbers, payment cards, customer accounts or production tokens.

## Requirements

- Physical Android and iOS devices for the highest-risk interruption cases.
- A safe staging backend or mock service for transactional checks.
- Access to lifecycle logs, network logs, crash reporting and backend correlation IDs where possible.
