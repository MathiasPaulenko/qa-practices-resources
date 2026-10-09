# AI Prompt: Test Cases from User Stories — Companion

Companion files for the [AI Prompt: Test Cases from User Stories](https://qapractices.com/prompts/generate-test-cases-from-user-stories-prompt) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full prompt template ready to copy-paste into any LLM. |
| `example-input.txt` | Example input: a discount-code user story with acceptance criteria and context. |
| `example-output.csv` | Example output with 8 test cases in CSV format, ready to import into TestRail. |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Replace the bracketed placeholders with your user story, acceptance criteria and context.
3. Run the prompt and review the generated suite — check that every case maps to an acceptance criterion.
4. Use `example-output.csv` as a reference format for importing into TestRail, Zephyr or Jira Xray.
5. Feed gaps back into the prompt ("add a negative case per permission level") and regenerate.

## Requirements

- Any LLM (ChatGPT, Claude, GitHub Copilot, or a local model).
- Optional: a test management tool that imports CSV or JSON (TestRail, Zephyr, Jira Xray).

## Notes

- Always review AI-generated test cases against the real application — the model can invent fields or UI elements that do not exist.
- Keep one user story per run; quality drops when several stories are combined in a single prompt.
- Treat the generated Risk Analysis as a first opinion, not a verdict — correct it against your defect history.
