# AI Prompt: Property-Based Testing Scenarios

Prompt template for generating property-based test scenarios from a function spec: named invariants, input generator strategies, falsifying edge cases, and framework sketches for Hypothesis, fast-check, or jqwik.

## Files

- `prompt-template.txt` — the prompt with placeholders for function name, signature, input domain, output contract, business rules, and count.
- `example-input.txt` — a filled example: `calculateDiscount(price, tier)` pricing function.
- `example-output.txt` — the full ten-property output for that input, plus a runnable Hypothesis sketch.

## Usage

1. Copy `prompt-template.txt` into your LLM.
2. Replace the bracketed variables — `example-input.txt` shows a realistic fill.
3. Keep the properties that would catch a real bug; drop the ones that restate the implementation.

Full article: https://qapractices.com/prompts/ai-prompt-property-based-testing
