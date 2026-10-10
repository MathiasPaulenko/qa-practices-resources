# AI Prompt: SQL Database Test Cases — Companion

Companion files for the [AI Prompt: SQL Database Test Cases](https://qapractices.com/prompts/ai-prompt-database-testing) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full schema-to-suite prompt, ready to copy-paste into any LLM. |
| `example-input.txt` | Example input: a PostgreSQL 16 `public.users` table with unique constraints, B-tree indexes and a 100 000-row estimate. |
| `example-output.csv` | The generated test cases as an importable CSV: id, title, category, priority, SQL, expected result and expected SQL outcome. |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Replace the bracketed placeholders with your engine version, DDL, indexes and row estimate.
3. Run it on one table at a time — pasting a whole schema returns shallow coverage.
4. Compare the output with `example-output.csv` to sanity-check the expected format.
5. Execute every generated query on a throwaway database before adding cases to a suite.

## Requirements

- Any LLM with room for the prompt plus your table DDL.
- Optional: a disposable database (Docker Postgres, for example) to verify the generated SQL.
