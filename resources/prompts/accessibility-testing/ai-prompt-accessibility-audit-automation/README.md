# AI Prompt to Automate WCAG Accessibility Tests — Companion

Companion files for the [AI Prompt to Automate WCAG Accessibility Tests](https://qapractices.com/prompts/ai-prompt-accessibility-audit-automation) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full accessibility-automation prompt, ready to copy-paste into any LLM. |
| `example-input.txt` | Example input: the PulseCare Patient Portal scenario (Angular 17.3, WCAG 2.2 AA, ADA Title III). |
| `example-output.md` | Fragments of the expected output: the `a11y.yml` CI workflow step and a Playwright focus-indicator test. |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Replace every bracketed placeholder with your real framework version, base URL, screen-reader matrix, and audit scope.
3. Run it once and compare the output shape with `example-output.md` — if the model skips deliverables, re-ask for the missing numbered item.
4. Run the generated suite locally before wiring the workflow into CI; first runs usually surface environment gaps.
5. Review every disabled axe rule in the generated config — each one should carry a justification comment.

## Requirements

- Any LLM that accepts a ~2k-token prompt (GPT-4-class models, Claude, Copilot Chat).
- To run the generated tests: Node 20+, Playwright, and a reachable staging URL.

## Notes

- Automated axe checks catch roughly a third of WCAG issues — keep the manual screen-reader scripts the prompt generates; they are not optional extras.
- Never point the generated suite at production; use staging.
- Do not paste real user data or credentials into the prompt.
