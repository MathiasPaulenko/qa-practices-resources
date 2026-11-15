# LLM Prompt Injection Testing Checklist — Companion Kit

Runnable companion for the [LLM Prompt Injection Testing Checklist](https://qapractices.com/checklists/llm-prompt-injection-testing-checklist). It packages the probe harness, the adversarial dataset and the output guardrail check from the resource into a pytest suite that runs fully offline against a mock LLM — or against a real endpoint when you set `LLM_ENDPOINT`.

## Files

| File | Purpose |
| --- | --- |
| `probe.py` | Chat-completions probe harness (`requests` 2.32+). Reads `LLM_ENDPOINT` from the environment. |
| `mock_llm.py` | Deterministic mock of a hardened model: refuses injection markers, answers benign input. |
| `guardrail.py` | `assert_no_disclosure` — fails if forbidden terms appear in the model output. |
| `dataset.yaml` | Adversarial prompts with `name`, `input` and `expectation` (`refuse` / `allow`). |
| `test_probe.py` | Parametrized pytest run over the dataset; mock by default, live endpoint via env var. |
| `requirements.txt` | Pinned dependencies (`requests`, `pytest`, `PyYAML`). |

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Offline run against the bundled mock
pytest test_probe.py -v

# Live run against a chat-completions endpoint
LLM_ENDPOINT=https://your-llm-gateway.internal/v1/chat pytest test_probe.py -v
```

## Requirements

- Python 3.10+
- `requests` 2.32+
- `pytest` 9.x
- `PyYAML` 6.x

## Notes

- The mock is a stand-in for a *hardened* model: it refuses the injection markers in `mock_llm.INJECTION_MARKERS`. A failing test against the mock means the harness or dataset is broken, not the model.
- To evaluate a vulnerable model, point `LLM_ENDPOINT` at a staging gateway and read the failures as findings — triage them with the severity ladder in the checklist.
- Extend `dataset.yaml` per release; keep one entry per attack vector and tag the file per model version.
