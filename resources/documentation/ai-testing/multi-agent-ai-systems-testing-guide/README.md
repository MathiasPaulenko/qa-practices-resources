# Multi-Agent AI Systems Testing Guide — Runnable Companion

Companion repository for the QAPractices resource
[Multi-Agent AI Systems Testing Guide](https://qapractices.com/documentation/multi-agent-ai-systems-testing-guide/)
([versión en español](https://qapractices.com/es/documentation/multi-agent-ai-systems-testing-guide/)).

`agent_kit.py` ships minimal pure-Python fixtures — a message bus, a
majority-vote function, a per-agent-namespaced shared tool, a wait-for
deadlock detector, a toy swarm and a retrying orchestrator — so the
pytest suite needs no LLM, no API key and no framework install.

## Layout

```text
agent_kit.py              message bus, voting, shared tool, deadlock detector, swarm, orchestrator
tests/test_multi_agent.py pytest 8.3 suite implementing the guide's test matrices
requirements.txt          pytest>=8.3 (only dependency)
```

## Run

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## What the tests cover

- **Message validation** — malformed payloads are rejected; out-of-order
  messages are re-sorted by sequence number.
- **Orchestration** — a research-then-write workflow runs both agents, and
  a flaky agent is retried until the run succeeds.
- **Consensus** — one Byzantine agent cannot flip an honest majority, and
  quorum blocks a decision when too few agents vote.
- **Conflicts** — shared-tool state stays isolated per agent, and a
  circular wait between two agents is flagged as a deadlock.
- **Emergent behavior** — the swarm's global metric converges over 100
  iterations and work continues after losing an agent.

All 12 tests pass offline with pytest 8.3 — every fixture is deterministic
so the suite is safe for CI.
