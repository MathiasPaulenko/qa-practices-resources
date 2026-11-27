# AI Prompt: Mobile App Test Scenarios — Companion

Companion files for the [AI Prompt: Mobile App Test Scenarios](https://qapractices.com/prompts/ai-prompt-mobile-app-test-scenarios) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full prompt template ready to copy-paste into any LLM. |
| `example-input.txt` | Example input: FitPulse, a React Native fitness app with its device and network context. |
| `example-output.csv` | Example output: 12 scenarios across lifecycle, offline sync, biometrics, push, interrupts, fragmentation, health permissions and cross-platform — importable into any CSV-capable test management tool. |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Replace the bracketed placeholders in the `App Under Test` and `Device and Environment Constraints` blocks with your real app context.
3. Run it and review each scenario's failure indicator — that field is what turns a row into a triage-ready bug report.
4. Use `example-output.csv` as the reference format for TestRail, Jira or Azure DevOps imports.
5. Re-run per platform when iOS/Android differences matter (push delivery, permission dialogs, background limits).

## Requirements

- Any LLM (ChatGPT, Claude, GitHub Copilot, or a local model).
- For execution: real devices or a farm (BrowserStack, Sauce Labs) plus the tool each scenario suggests (Appium, XCUITest, Espresso, Detox, Maestro).

## Notes

- Fill the device list with the models your analytics actually show — generic lists produce generic scenarios.
- Keep at least one edge case per category; interrupt and lifecycle rows are where real crashes live.
- Review the output with a senior QA before it reaches the test repository: LLMs still miss platform quirks like Android's exact-alarm restrictions.
