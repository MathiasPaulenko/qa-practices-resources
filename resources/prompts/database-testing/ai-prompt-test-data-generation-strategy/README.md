# AI Prompt: Test Data Generation Strategy — Companion

Companion files for the [AI Prompt: Test Data Generation Strategy](https://qapractices.com/prompts/ai-prompt-test-data-generation-strategy) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full strategy prompt, ready to copy-paste into any LLM. |
| `example-input.txt` | Example input: an e-commerce backend on PostgreSQL 16 with 2M order items. |
| `example-output.md` | Fragment of the generated entity plan for that input (five entities with volumes and constraints). |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Replace every bracketed placeholder — stores, volumes, domain, relationships, formats — with your real values.
3. Run it and compare the output shape with `example-output.md`; if a requirement area comes back thin, re-ask for that numbered item.
4. Paste your real schema and relationship map alongside the prompt for entities that name actual tables.
5. Keep a fixed random seed in the deliverables so datasets stay reproducible.

## Requirements

- Any LLM that accepts a ~1.2k-token prompt (GPT-4-class models, Claude, Copilot Chat).
- To execute the generated scripts: Python with Faker (or JavaFaker / faker-js) and the target database.

## Notes

- The resource page also ships a tactical variant that outputs ready-to-load datasets instead of a strategy — use it when you need data now, not a plan.
- Never paste real customer data or production connection strings into the prompt.
