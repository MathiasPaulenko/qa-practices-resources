# AI Prompt: Security Risk & Threat Assessment — Companion

Companion files for the [AI Prompt: Security Risk & Threat Assessment](https://qapractices.com/prompts/ai-prompt-security-testing) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full prompt template ready to copy-paste into any LLM. |
| `example-input.txt` | Example input: an online banking app with stack, auth method, assets, flows and scope. |
| `example-output.csv` | Example risk register with 6 scored threats (STRIDE + OWASP mapping, likelihood x impact). |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Replace the bracketed placeholders with your system context, assets, data flows and scope.
3. Run the prompt and review the register — read the Assumptions section first, that is where the model confesses what it guessed.
4. Compare the rows with `example-output.csv` to sanity-check the expected format and scoring.
5. Feed the top risks into the [security test case generation prompt](https://qapractices.com/prompts/ai-prompt-security-test-case-generation) to turn them into executable cases.

## Requirements

- Any LLM (ChatGPT, Claude, GitHub Copilot, or a local model).
- Optional: a spreadsheet or GRC tool that imports CSV if you want to keep the register under version control.

## Notes

- Only assess systems you are authorized to evaluate; keep the Authorization line in the prompt.
- Describe architecture, data types and flows — never paste real credentials, hostnames of sensitive systems or customer data.
- Likelihood and impact are model estimates: validate the top rows against your own exposure data before committing test effort.
- Re-run the assessment when the architecture changes; a risk register is a snapshot.
