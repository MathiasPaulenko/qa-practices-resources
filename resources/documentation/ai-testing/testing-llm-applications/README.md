# Testing LLM Applications Companion

Companion resource for [Testing LLM Applications](https://qapractices.com/documentation/testing-llm-applications). A runnable pytest suite implementing the four validation layers from the guide: schema contract, semantic similarity, adversarial injection probes and golden-dataset regression.

## Files

| File | Layer | What it does | Stack |
|------|-------|--------------|-------|
| `support_bot.py` | — | Deterministic stub of an LLM endpoint — replace `ask()` with your real client | Python 3.9+ |
| `test_schema.py` | 1 | Validates response shape and citation contract | jsonschema 4.22+ |
| `test_semantic.py` | 2 | Embedding-similarity floor vs expected answer | sentence-transformers, all-MiniLM-L6-v2 |
| `test_injection.py` | 3 | Parametrized OWASP LLM01 probes | pytest 8.x |
| `test_golden_regression.py` + `golden_dataset.jsonl` | 4 | Scores real questions against must-contain keywords | pytest 8.x |

## Quick Start

```bash
pip install pytest jsonschema numpy sentence-transformers
pytest -v

# Layers that run without the embedding model download:
pytest test_schema.py test_injection.py test_golden_regression.py -v
```

The stub makes every layer runnable offline — point `ask()` at your real endpoint and the same tests apply.

## Requirements

- Python 3.9+
- `pytest`, `jsonschema` for layers 1, 3, 4
- `sentence-transformers` + `numpy` for layer 2 (model downloads ~90MB once)
