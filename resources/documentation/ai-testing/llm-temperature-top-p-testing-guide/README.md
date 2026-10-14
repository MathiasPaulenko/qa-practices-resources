# LLM Temperature & Top-P Testing Guide — Runnable Companion

Companion repository for the QAPractices resource
[LLM Temperature & Top-P Testing Guide](https://qapractices.com/documentation/llm-temperature-top-p-testing-guide/)
([versión en español](https://qapractices.com/es/documentation/llm-temperature-top-p-testing-guide/)).

Two modes: `sweep.py` runs the temperature x top-p grid against the real
OpenAI API, and `mock_llm.MockClient` simulates the same sampling behavior
offline so the pytest suite needs no API key.

## Layout

```text
sweep.py            temperature x top-p grid runner (openai 1.x client or mock)
mock_llm.py         deterministic mock client simulating sampling
tests/test_sweep.py pytest 8.3 suite for the sweep behavior
requirements.txt    openai>=1.54, pytest>=8.3
```

## Run

```bash
pip install -r requirements.txt

# offline tests (no API key needed)
pytest tests/ -v

# offline sweep
python sweep.py --mock

# real API sweep
export OPENAI_API_KEY=sk-...
python sweep.py
```

## What the tests cover

- **Determinism at temp 0** — ten runs, one unique output.
- **Diversity at temp 1.0** — ten runs, more than one unique output.
- **Top-p truncation** — `top_p=0.2` caps reachable variants at two.
- **Grid coverage** — every (temperature, top-p) cell produces a count.
- **Repetition depth** — 20 runs reveal at least as much variation as 5.
- **Prompt cell** — the sweep honors the prompt argument per cell.

All six tests pass offline with pytest 8.3 — the mock client makes
variation deterministic while preserving the parameter semantics.
