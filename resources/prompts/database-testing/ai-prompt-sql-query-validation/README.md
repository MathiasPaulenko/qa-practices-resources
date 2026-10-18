# AI Prompt: SQL Query Validation — Companion

Companion files for the [AI Prompt: SQL Query Validation](https://qapractices.com/prompts/ai-prompt-sql-query-validation) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full query-validation prompt, ready to copy-paste into any LLM. |
| `example-input.sql` | Example input: PostgreSQL 16.4 DDL for `users`/`orders` plus a report query with planted defects (dialect error, injection-prone binding, implicit join, NULL trap, non-sargable predicates). |
| `expected-findings.md` | The reference findings table (F-01..F-08) and corrected query — use it to check whether a model's output ignored the context. |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Replace the bracketed placeholders with your engine version, DDL, row counts and SLA.
3. Validate one query per run — a multi-statement script gets a shallow pass on all of them.
4. Compare the output against `expected-findings.md`: a good run catches F-01 and F-02 first.
5. Execute the corrected query on a throwaway database before merging anything.

## Requirements

- Any LLM with room for the prompt plus your DDL.
- Optional: a disposable database (Docker Postgres, for example) to verify the corrected SQL and run `EXPLAIN (ANALYZE, BUFFERS)`.
