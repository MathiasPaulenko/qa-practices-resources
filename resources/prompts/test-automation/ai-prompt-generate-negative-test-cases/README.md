# AI Prompt: Negative Test Cases — Companion

Companion files for the [AI Prompt: Negative Test Cases](https://qapractices.com/prompts/ai-prompt-generate-negative-test-cases) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full negative-testing prompt, ready to copy into an LLM. |
| `example-input.txt` | A realistic API contract context: endpoint, stack, validation rules and constraints. |
| `example-output.md` | A realistic output fragment: 12 prioritized cases covering all five categories. |
| `negative-payloads.csv` | A seed list of exact payload values per category — usable as a CSV data source for parameterized tests. |

## Usage

1. Copy `prompt-template.txt` into your LLM.
2. Replace the bracketed placeholders with your real contract, stack, validation rules and constraints.
3. Compare the response with `example-output.md`; a good answer uses exact input values, names observable expected behavior, tiers rows by risk and flags ambiguous contract points.
4. Use `negative-payloads.csv` as a starting data source for parameterized tests — payload, field hint and expected probe per row.
5. Rows marked "spec silent" or ambiguous are contract findings: fix the API contract, not the test.

## Requirements

- No tools required; the output is a case table.
- Injection-shaped payloads are test fixtures to type into fields — never run them against a live target.
- A staging environment for executing the stateful and concurrency rows.
