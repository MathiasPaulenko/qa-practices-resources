# AI Prompt: Rate Limiting Test Scenarios — Companion

Companion files for the [AI Prompt: Rate Limiting Test Scenarios](https://qapractices.com/prompts/ai-prompt-rate-limiting-testing) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full rate limiting test design prompt, ready to copy into an LLM. |
| `example-input.txt` | A filled-in context: PaymentAPI, token bucket, Redis shared counter, 3 tiers, API-key counting. |
| `example-output.md` | A realistic output fragment: burst boundary and shared-counter scenarios, boundary math for the given limit, and a fail-closed failover test. |

## Usage

1. Copy `prompt-template.txt` into your LLM.
2. Fill the limiter context — name your algorithm, counting key and where enforcement lives; skip what doesn't apply.
3. Decide fail-open vs fail-closed *before* running it — the prompt asks for the expectation, not a shrug.
4. Compare the response with `example-output.md`; bypass scenarios should match your counting key and boundary math should use your real numbers.
5. Re-run after Redis upgrades, gateway migrations or CDN rule changes.
