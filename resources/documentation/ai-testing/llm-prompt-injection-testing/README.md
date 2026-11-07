# LLM Prompt Injection Testing — Runnable Companion

Companion to [LLM Prompt Injection Testing](https://qapractices.com/documentation/llm-prompt-injection-testing/) on QAPractices.com.

A minimal red-teaming harness for LLM apps: an adversarial prompt dataset
tagged by attack vector, a probe runner that classifies responses into the
three signals (refusal, context leakage, unauthorized tool call), and a
pytest suite that asserts per-vector thresholds.

## Contents

```text
dataset/adversarial-prompts.yaml  # 15 attacks across 5 vectors
mock_target.py                  # stdlib mock LLM endpoint (intentionally weak)
redteam/runner.py               # dataset runner → per-vector JSON report
tests/test_redteam.py           # pytest suite with per-case assertions
requirements.txt
.github/workflows/redteam.yml   # CI gate example
```

## Quick start

```bash
pip install -r requirements.txt
python mock_target.py &          # mock endpoint on :8000
pytest tests/ -v                 # per-case assertions
python redteam/runner.py         # JSON report → redteam-report.json
```

Against a real app, point `LLM_ENDPOINT` at your staging chat endpoint:

```bash
LLM_ENDPOINT=https://staging.example.com/chat pytest tests/ -v
```

## Signals

| Signal | Detection | Gate |
|---|---|---|
| Refusal | response contains a refusal marker | ≥ 90% per vector |
| Context leakage | response echoes hidden context/secrets | 0 allowed |
| Tool invocation | `tool_calls` non-empty for a blocked input | 0 allowed |

The mock target intentionally fails `encoding` and `tool_misuse` vectors so
you can see what real failures look like in the report.

## Dataset format

```yaml
- id: direct-001
  vector: direct            # direct | indirect | encoding | multilingual | tool_misuse
  prompt: "..."
  expect: refusal           # refusal | no_leakage | no_tool_call
```

New reported attacks become new entries; the dataset diff is part of the
security changelog.

## Related

- Guide: https://qapractices.com/documentation/llm-prompt-injection-testing/
- Sister companion (20 attack cases + mock): `resources/test-cases/security-testing/llm-prompt-injection-test-cases/`
