# AI Prompt: Mobile Test Matrix — Companion

Companion files for the [AI Prompt: Mobile Test Matrix](https://qapractices.com/prompts/ai-prompt-generate-mobile-test-matrix) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full mobile test-matrix generation prompt, ready to copy into an LLM. |
| `example-input.txt` | A realistic mobile app context: platforms, markets, constraints and test capacity. |
| `example-output.md` | A realistic output fragment: assumptions, coverage axes, P0/P1/P2 tiers, execution map and gap analysis. |
| `matrix-template.csv` | The generated matrix as a CSV — tier, device, OS, screen, network, locale, execution channel and rationale per row. |

## Usage

1. Copy `prompt-template.txt` into your LLM.
2. Replace the bracketed placeholders with your real app, markets, supported OS range and test capacity.
3. Compare the response with `example-output.md`; a good answer states its assumptions, tiers rows by reason, maps each tier to a runner and admits its gaps.
4. Use `matrix-template.csv` as the working document: one row per device+OS+screen+network combo with its tier and execution channel.
5. Validate P0 against real analytics or last quarter's crash reports before locking the matrix — market-share estimates are a draft, not ground truth.

## Requirements

- No tools required; the output is a planning document.
- Optional: Firebase Test Lab, BrowserStack or a device shelf to execute the tiers.
- Device analytics (Firebase, GA4 or Play Console/App Store Connect) make the picks real instead of estimated.
