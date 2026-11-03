"""Runnable pytest suite for the multi-agent testing guide examples.

Run with: pytest tests/ -v   (pytest >= 8.3, no API key or LLM needed)
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_kit import (  # noqa: E402
    Agent,
    MessageBus,
    Orchestrator,
    SharedTool,
    SwarmSystem,
    detect_deadlock,
    majority_vote,
)


# --- 1. Agent communication ---------------------------------------------

def test_rejects_malformed_message():
    bus = MessageBus()
    malformed = {"from": "agent_a"}  # missing required "payload"
    with pytest.raises(ValueError, match="payload"):
        bus.validate(malformed)


def test_agent_reorders_out_of_sequence_messages():
    bus = MessageBus()
    bus.deliver({"seq": 2, "from": "agent_b", "payload": "second"})
    bus.deliver({"seq": 1, "from": "agent_b", "payload": "first"})
    received = bus.consume("agent_a")
    assert [m["payload"] for m in received] == ["first", "second"]


# --- 2. Task delegation / orchestration ---------------------------------

def test_research_then_write_workflow():
    orch = Orchestrator(agents={
        "research": lambda task: {"citations": 3},
        "writer": lambda task: {"output": "Summary of the latest QA trends"},
    })
    result = orch.run("Write a summary of the latest QA trends")
    assert result["results"]["research"]["citations"] >= 2
    assert "summary" in result["results"]["writer"]["output"].lower()


def test_orchestrator_retries_on_agent_failure():
    calls = {"count": 0}

    def flaky_agent(task):
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("agent crashed")
        return {"output": "done"}

    orch = Orchestrator(agents={"fragile": flaky_agent}, max_retries=2)
    result = orch.run("simple task")
    assert result["status"] == "success"
    assert calls["count"] == 2


# --- 3. Consensus and voting --------------------------------------------

def test_byzantine_agent_cannot_flip_majority():
    votes = ["approve", "approve", "approve", "reject"]  # 3 honest + 1 Byzantine
    assert majority_vote(votes) == "approve"


def test_quorum_blocks_decision_without_participation():
    assert majority_vote(["approve", "approve"], required_quorum=3) == "no_consensus"


def test_empty_votes_return_no_consensus():
    assert majority_vote([]) == "no_consensus"


# --- 4. Conflict resolution / deadlock -----------------------------------

def test_tool_state_isolated_between_agents():
    tool = SharedTool()
    tool.use(agent="agent_1", action="set", value=10)
    tool.use(agent="agent_2", action="set", value=20)
    assert tool.read("agent_1") == 10
    assert tool.read("agent_2") == 20


def test_detects_circular_wait():
    wait_for = {"agent_a": "agent_b", "agent_b": "agent_a"}
    result = detect_deadlock(wait_for)
    assert result["deadlock"] is True
    assert "agent_a" in result["involved_agents"]


def test_no_deadlock_in_linear_chain():
    wait_for = {"agent_a": "agent_b", "agent_b": "agent_c"}
    assert detect_deadlock(wait_for)["deadlock"] is False


# --- 6. Emergent behavior / swarm ----------------------------------------

def test_swarm_stable_over_iterations():
    swarm = SwarmSystem(agents=[Agent() for _ in range(5)])
    values = []
    for _ in range(100):
        swarm.step()
        values.append(swarm.global_metric())
    # Metric should stabilize, not diverge
    assert max(values[-10:]) - min(values[-10:]) < 0.1


def test_fault_tolerance_after_losing_agent():
    swarm = SwarmSystem(agents=[Agent() for _ in range(5)])
    initial_work = swarm.total_work_done()
    swarm.remove_random_agent()
    for _ in range(50):
        swarm.step()
    assert swarm.total_work_done() > initial_work
