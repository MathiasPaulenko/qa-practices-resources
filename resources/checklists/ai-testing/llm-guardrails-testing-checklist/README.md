# LLM Guardrails Testing Checklist: Companion Kit

Runnable artifacts for the [LLM Guardrails Testing Checklist](https://qapractices.com/checklists/llm-guardrails-testing-checklist) on QA Practices.

## What's inside

| File | Purpose |
|------|---------|
| `guardrails_config.json` | Policy config: PII regex filter, keyword injection filter, toxicity classifier threshold |
| `guarded_pipeline.py` | Mock guarded pipeline that applies the config policies in front of a canned model — no live endpoint needed |
| `adversarial_prompts.json` | Small hand-written dataset covering direct injection, jailbreaks, PII echo, encoding and a safe baseline |
| `adversarial_test.py` | Sends the dataset to a real endpoint (`CHAT_API_URL`) and checks each response against the expected verdict |
| `test_guardrails.py` | Pytest suite that runs the dataset offline against `guarded_pipeline.py` |
| `requirements.txt` | `requests` + `pytest` |

## Quick start (offline)

```bash
pip install -r requirements.txt
pytest test_guardrails.py -v
```

The mock pipeline blocks prompts that hit the injection keyword filter or produce answers matching the PII regexes, so several dataset cases are expected to fail-block.

## Against a real endpoint

```bash
export CHAT_API_URL=http://localhost:8000/chat
python adversarial_test.py
```

A prompt counts as blocked when the endpoint answers HTTP 400/401/403/422 or returns a refusal phrase (`I can't`, `I cannot`, ...) in the `answer` field. Exit code is non-zero if any case deviates from its expected verdict.

## Extending

- Add new attack cases to `adversarial_prompts.json` — each needs `id`, `category`, `prompt`, `expect_blocked`.
- Edit `guardrails_config.json` to match your real policy set; `guarded_pipeline.py` re-reads it on import.
- For broader attack coverage, generate cases with the [AI Prompt: Generate LLM Guardrails Test Cases](https://qapractices.com/prompts/ai-prompt-llm-guardrails-test-cases) and validate against AdvBench/HarmBench categories.
