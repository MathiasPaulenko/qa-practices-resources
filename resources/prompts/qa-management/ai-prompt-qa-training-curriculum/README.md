# AI Prompt: Generate a QA Training Curriculum — Companion

Companion files for the [AI Prompt: Generate a QA Training Curriculum](https://qapractices.com/prompts/ai-prompt-qa-training-curriculum) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full curriculum design prompt, ready to copy into an LLM. |
| `example-input.txt` | A filled-in context: 3 juniors + 1 mid QA, e-commerce checkout, Playwright + GitHub Actions, API-testing gap. |
| `example-output.md` | A realistic output fragment: Module 2 with objectives, three labs on the real stack, CI assessment and a checkpoint with a failure path. |

## Usage

1. Copy `prompt-template.txt` into your LLM.
2. Fill the context block — name exact tools and versions, and state the skill gap behaviorally ("nobody writes API tests", not "improve automation").
3. Compare the response shape with `example-output.md`; every module should carry objectives, labs on *your* stack and a checkpoint with a failure path.
4. Reject modules that don't serve the gap — the prompt is instructed to drop them.
5. Re-run when the gap closes or the stack changes.
