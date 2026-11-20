# LLM Output Quality Evaluation Harness

Offline companion for the [LLM Output Quality Testing Checklist](https://qapractices.com/checklists/llm-output-quality-testing-checklist). It scores generated answers on the checklist's dimensions — consistency, factual grounding, contradiction and relevance — over a versioned prompt corpus, without needing paid APIs or network access.

## What's inside

| File | Purpose |
|---|---|
| `eval_prompts.json` | Versioned eval corpus: 8 prompts mapped to checklist dimensions with thresholds |
| `mock_model_outputs.json` | Recorded model answers (3 samples per prompt) for offline runs |
| `quality_evaluator.py` | Deterministic scorers: consistency, grounding, contradiction, relevance, refusal |
| `run_evaluation.py` | Runner; scores `mock_model_outputs.json` offline, or queries `CHAT_API_URL` live |
| `test_quality_evaluator.py` | pytest suite for the scorers |

## Quick start

```bash
python -m pytest -v          # scorer unit tests
python run_evaluation.py     # offline eval over recorded outputs
```

Live mode against a real endpoint (requires `requests`):

```bash
export CHAT_API_URL=http://localhost:8000/chat
python run_evaluation.py
```

Each prompt is sampled three times so the consistency scorer sees real
sampling variance. A case fails when its score drops below the threshold
in `eval_prompts.json`; add production failures to the corpus so the eval
gets harder over time, not easier.
