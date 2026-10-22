# AI Agent Conversation Test Cases — Companion

Companion resource for [AI Agent Conversation Test Cases: Multi-Turn & Tools](https://qapractices.com/test-cases/ai-agent-conversation-test-cases/).

## Contents

- `agent_simulator.py` — stdlib-only deterministic model of the agent turn pipeline described in the article: injection/harmful-content guardrails, session-scoped context retention, a `ToolRegistry` with injectable failures, missing-parameter clarification and repeat-message loop detection. No model API calls — the rules stand in for the LLM so the suite runs fully offline.
- `tests/conftest.py` — puts the simulator on `sys.path`.
- `tests/test_agent_simulator.py` — executable subset of the article's cases: greeting (TC-001), context retention (TC-002), prompt injection (TC-011), harmful content (TC-012), tool failure (TC-014), circular conversation (TC-018), empty message (TC-021), session isolation (TC-024), missing tool params (TC-026) and multi-parameter tool call (TC-004).

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Expected output: `10 passed`.

In a real suite you'd point `send_message` at the agent's HTTP endpoint and keep the same assertions — the simulator exists so the properties under test (recall, refusal, parameter elicitation, isolation) are visible without a live model.

## Related

- Article EN: https://qapractices.com/test-cases/ai-agent-conversation-test-cases/
- Article ES: https://qapractices.com/es/test-cases/ai-agent-conversation-test-cases/
