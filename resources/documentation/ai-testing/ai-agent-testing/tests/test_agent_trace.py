from agent import run_agent


def test_agent_refund_flow():
    trace = run_agent("I want a refund for order 12345")
    tool_calls = [step["tool"] for step in trace]
    assert "lookup_order" in tool_calls
    assert any("refund" in str(step) for step in trace)
    assert trace[-1]["status"] == "completed"
    assert trace[-1]["human_handoff"] is False
