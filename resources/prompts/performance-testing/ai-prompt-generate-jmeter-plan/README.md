# AI Prompt: JMeter Test Plan — Companion

Companion files for the [AI Prompt: JMeter Test Plan](https://qapractices.com/prompts/ai-prompt-generate-jmeter-plan) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full JMeter test-plan generation prompt, ready to copy into an LLM. |
| `example-input.txt` | A realistic checkout API context with load model, SLA and JMeter settings. |
| `example-output.md` | A realistic output fragment: thread group, samplers, timers, assertions, listeners and the non-GUI execution line. |
| `users.csv` | Sample CSV dataset for the CSV Data Set Config (test users only, no real credentials). |

## Usage

1. Copy `prompt-template.txt` into your LLM.
2. Replace the bracketed placeholders with your real API, load model, SLA and JMeter version.
3. Compare the response with `example-output.md`; a good answer names thread groups, per-sampler correlation, assertions, a data strategy and the `jmeter -n -t` execution line.
4. Build the plan in the JMeter GUI or a `.jmx` editor, then run a 10-user, 2-minute smoke before the full load.
5. Run load tests only against staging or a dedicated performance environment. Never use production credentials, tokens or customer data.

## Requirements

- Apache JMeter 5.6.3 (or the version stated in the prompt output).
- A staging environment that tolerates the planned load.
- A CSV dataset sized to the thread count (see `users.csv` for the format).
