# AI Agent Testing — Companion Files

Runnable examples from [AI Agent Testing Guide: Autonomous & Multi-Agent](https://qapractices.com/documentation/ai-agent-testing/).

## Contents

- `tests/test_llm_output_eval.py` — validates a support chatbot answer against a JSON schema and requires citations (Python 3.11, pytest 8.2, jsonschema 4.22).
- `tests/test_agent_trace.py` — replays a recorded agent trace and asserts tool-call sequence and final state.
- `tests/requirements.txt` — pinned dependencies.

## Setup

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r tests/requirements.txt
```

`qa_assistant` and `agent` are placeholders for your own client wrappers around the model endpoint and agent harness — replace the imports with your implementation before running.
