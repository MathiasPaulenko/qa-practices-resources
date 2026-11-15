# AI Prompt: Mutation Testing Strategy — Companion

Companion files for the [AI Prompt: Mutation Testing Strategy](https://qapractices.com/prompts/ai-prompt-mutation-testing-strategy) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full strategy prompt, ready to copy-paste into any LLM. |
| `example-input.txt` | Example input: a Java 21 payment module measured with PIT on GitHub Actions. |
| `pitest-pom.xml` | PIT (pitest-maven 1.30.x) plugin block with STRONGER mutators, a 75% gate and history files. |
| `stryker.conf.json` | StrykerJS 10.x config with `thresholds.break`, incremental mode and a scoped `mutate` list. |
| `mutmut-setup.cfg` | mutmut 3.x `setup.cfg` section scoped to one package, with excluded paths. |

## Usage

1. Copy `prompt-template.txt` into your LLM.
2. Replace the bracketed placeholders using `example-input.txt` as a reference for detail level.
3. Take the config file that matches your stack and adapt package names, thresholds and paths.
4. Run a first scoped mutation run on one critical module before enabling the CI gate — the baseline run tells you where the equivalent mutants live.
5. Wire `thresholds.break` / `mutationThreshold` into CI only after the first triage, or the gate blocks on noise.

## Requirements

- Java/JVM: Maven or Gradle plus pitest-maven 1.30.x.
- JS/TS: Node.js 22+ and `@stryker-mutator/core` 10.x with your test runner plugin.
- Python: mutmut 3.x (`pip install mutmut`) and pytest.
- A CI runner where the mutation job can run in parallel threads (PIT `threads`, Stryker `concurrency`).

## Notes

- Equivalent mutants are expected (roughly 5-15% of survivors): document and exclude them instead of writing tests for trivia.
- Keep the gate on the score delta per module, not on a flat repo-wide number.
- Never paste real credentials, PII or production data into the prompt.
- The related resource keeps the same content in Spanish at [qapractices.com/es](https://qapractices.com/es/prompts/ai-prompt-mutation-testing-strategy).
