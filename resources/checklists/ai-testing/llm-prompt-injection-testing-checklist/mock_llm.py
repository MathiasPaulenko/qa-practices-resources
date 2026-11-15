"""Deterministic mock of a hardened LLM endpoint for offline testing.

The mock refuses known injection markers and answers everything else with a
canned reply, so the pytest suite can validate the harness without a real
model. Replace with your staging endpoint for live runs.
"""

INJECTION_MARKERS = (
    "ignore previous instructions",
    "ignore all previous instructions",
    "repeat the system prompt",
    "you are dan",
    "bypass safety",
    "training data",
    "decode and follow",
)


def mock_llm(system_prompt, user_input):
    """Return a refusal for injected inputs, a canned reply otherwise."""
    text = user_input.lower()
    if any(marker in text for marker in INJECTION_MARKERS):
        return "I can't help with that request."
    return "Sure, here is the answer based on your request."
