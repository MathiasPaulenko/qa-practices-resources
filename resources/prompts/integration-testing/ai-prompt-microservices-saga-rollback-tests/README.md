# AI Prompt: Microservices Saga Rollback Tests — Companion

Companion files for the [AI Prompt: Generate Microservices Saga Rollback Tests](https://qapractices.com/prompts/ai-prompt-microservices-saga-rollback-tests) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full saga rollback prompt, ready to copy-paste into any LLM. |
| `example-input.txt` | Example input: a four-service e-commerce order saga with choreography on Kafka, Postgres saga state and idempotency keys. |
| `example-output.csv` | The generated test cases as an importable CSV: id, name, saga type, services, failure scenario, preconditions, expected result, pass/fail criteria, severity and test type. |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Replace the bracketed placeholders with your saga topology: saga type, services, broker, orchestration framework, state persistence, idempotency, timeouts, retries, DLQ, monitoring and business context.
3. Run it per saga, not per system — a whole architecture comes back with generic coverage.
4. Compare the output with `example-output.csv` to sanity-check the expected format.
5. Verify every generated case against real broker behavior (redelivery, partitions, consumer crashes) before adding it to a suite.

## Requirements

- Any LLM with room for the prompt plus your saga description.
- Optional: a staging environment with Testcontainers or Toxiproxy to turn the generated cases into executable tests.
