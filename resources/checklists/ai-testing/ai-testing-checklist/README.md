# AI Testing Checklist — Runnable Companion

Companion repository for the QAPractices resource
[AI Testing Checklist: LLM, Hallucination, Bias & Safety](https://qapractices.com/checklists/ai-testing-checklist/)
([versión en español](https://qapractices.com/es/checklists/ai-testing-checklist/)).

Two modes: `eval_runner.py` runs the guardrail dataset against the real
OpenAI API, and `mock_llm.MockClient` supplies deterministic answers so
the pytest suite works offline with no API key.

## Layout

```text
eval_runner.py          expected/forbidden phrase checker (openai 1.x or mock)
mock_llm.py             deterministic mock client mimicking the OpenAI API
guardrail_dataset.json  starter dataset: input, expected phrases, forbidden phrases
tests/test_eval_runner.py pytest 8.3 suite for the runner behavior
requirements.txt        openai>=1.54, pytest>=8.3
```

## Run

```bash
pip install -r requirements.txt

# offline tests (no API key needed)
pytest tests/ -v

# offline dataset run against the mock
python eval_runner.py --mock

# real API run
export OPENAI_API_KEY=sk-...
python eval_runner.py --model gpt-4o-mini
```

## What the tests cover

- **Expected phrases pass** — answer containing the required terms evaluates clean.
- **Missing expected content fails** — AssertionError when the answer omits a required term.
- **Forbidden content fails** — AssertionError when a banned phrase appears.
- **Case-insensitive matching** — uppercase answers still match lowercase patterns.
- **Dataset reporting** — every case reports pass/fail without stopping the run.
- **Failure isolation** — a failing case is reported, not raised, by `run_dataset`.

All six tests pass offline with pytest 8.3 — the mock keeps the runner
deterministic while preserving the OpenAI client interface.
