# AI Prompt: Cloud Infrastructure Testing — Companion

Companion files for the [AI Prompt: Cloud Infrastructure Testing](https://qapractices.com/prompts/ai-prompt-cloud-infrastructure-testing) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full pre-apply IaC review prompt, ready to copy-paste into any LLM. |
| `example-input.txt` | Example input: a two-tier Terraform module with SSH open to `0.0.0.0/0`, an unencrypted RDS instance, and a single-AZ autoscaling group. |
| `example-output.csv` | The findings table as importable CSV: resource, finding, minimal fix, verification command, severity. |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Replace the bracketed placeholders with your module, provider versions, environment, compliance target and blast radius budget.
3. Run it on one module or one diff at a time — pasting a whole repo returns generic advice.
4. Compare the output with `example-output.csv` to sanity-check the expected format and severity scale.
5. Confirm every row with Checkov or `terraform plan` before applying a suggested fix; re-run after each landed change.

## Requirements

- Any LLM with room for the prompt plus a few hundred lines of IaC (GPT-4-class models, Claude, Copilot Chat).
- Optional: a spreadsheet or tracker that imports CSV if you want the findings under version control.

## Notes

- Severity is the order to fix in, not a compliance verdict — always confirm with the real scanners.
- Never paste real credentials, account IDs, hostnames or customer data into the prompt.
- The related resource keeps the same content in Spanish at [qapractices.com/es](https://qapractices.com/es/prompts/ai-prompt-cloud-infrastructure-testing).
