# AI Prompt: Mobile App Test Plan — Companion

Companion files for the [AI Prompt: Mobile App Test Plan](https://qapractices.com/prompts/ai-prompt-mobile-app-testing) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full prompt template ready to copy-paste into any LLM. |
| `example-input.txt` | Example input: MedDrop, a React Native prescription-delivery app with its device matrix. |
| `example-output.csv` | Example output: 9 test cases covering biometrics, push, offline sync, compatibility, performance and Crashlytics — importable into any CSV-capable test management tool. |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Fill the `App and Environment` block with your real devices, farm and providers.
3. Run it and review the plan — every case should carry an evidence column entry.
4. Use `example-output.csv` as the reference format for TestRail, Jira or Azure DevOps imports.
5. Feed gaps back into the prompt ("add a foldable unfold case") and regenerate.

## Requirements

- Any LLM (ChatGPT, Claude, GitHub Copilot, or a local model).
- A real-device source for execution: BrowserStack, Sauce Labs, or a physical device pool.

## Notes

- Fill the device matrix with the models your analytics actually show — farm sessions on unused devices are wasted budget.
- Keep the farm session ID column: it is what turns a failure into a replayable session.
- Treat iOS and Android permission dialogs as separate cases — they behave differently enough to matter.
