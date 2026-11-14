# AI Prompt: Generate GraphQL Subscription Test Cases — Companion

Companion files for the [AI Prompt: Generate GraphQL Subscription Test Cases](https://qapractices.com/prompts/ai-prompt-graphql-subscription-test-cases) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full subscription test-case prompt, ready to copy-paste into any LLM. |
| `example-input.txt` | Example input: a real-time chat backend on Apollo Server 4 with graphql-transport-ws, JWT, and Redis pub/sub. |
| `example-output.md` | Fragment of the generated test matrix for that input (six cases with severities). |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Replace every bracketed placeholder — server, transport, subscription protocol, auth, pubsub, scale — with your real values.
3. Run it and compare the output shape with `example-output.md`; if a coverage area comes back thin, re-ask for that numbered item.
4. Paste your actual subscription schema alongside the prompt for cases that name real fields.
5. Review severities before filing — a dropped auth check is Critical even if the model tags it Medium.

## Requirements

- Any LLM that accepts a ~1.5k-token prompt (GPT-4-class models, Claude, Copilot Chat).
- To execute the generated cases: a GraphQL server with subscriptions (Apollo Server 4, Yoga, Mercurius, or graphql-ws) and a reachable environment.

## Notes

- `graphql-ws` and `graphql-transport-ws` are different protocols — state which your server runs or the reconnection cases will target the wrong message flow.
- The prompt covers subscriptions only; pair it with query/mutation test resources for full API coverage.
- Never paste real credentials or production endpoints into the prompt.
