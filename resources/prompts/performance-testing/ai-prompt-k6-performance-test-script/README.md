# AI Prompt: Generate a k6 Performance Test Script

Companion files for the QAPractices prompt
[Generate a k6 Performance Test Script](https://qapractices.com/prompts/ai-prompt-k6-performance-test-script/)
([versión en español](https://qapractices.com/es/prompts/ai-prompt-k6-performance-test-script/)).

## Contents

| File | Purpose |
|---|---|
| `prompt.md` | The prompt, ready to paste into ChatGPT, Claude or any LLM. |
| `example-input.txt` | A filled-in variable block (checkout service) you can adapt. |
| `load-test.js` | Example output: staged load test with `ramping-vus`, OAuth2 `setup()`, `SharedArray` test data, custom metrics and SLA thresholds. |
| `spike-test.js` | Spike variant: fast ramp to peak VUs, short hold, drop and recovery window. |
| `users.json` | Sample test data read by the scripts via `SharedArray`. |

## Usage

1. Copy `prompt.md` into your LLM and replace the bracketed placeholders — `example-input.txt` shows a realistic fill.
2. Or run the generated scripts directly with k6 1.x:

```bash
export BASE_URL=https://api-staging.example.com
export CLIENT_ID=your-client-id
export CLIENT_SECRET=your-client-secret

k6 run load-test.js
k6 run spike-test.js
```

The scripts expect `users.json` next to them and OAuth2 client-credentials auth; swap `setup()` for a static token or API key if your service uses one.

## Requirements

- k6 1.x (`k6 version`)
- A reachable `BASE_URL` implementing `POST /oauth/token`, `GET /products`, `POST /cart`, `POST /checkout`
