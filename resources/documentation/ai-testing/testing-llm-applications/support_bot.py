"""Stub LLM application — replace `ask()` with your real client call.

The tests exercise the interface, not the model, so this deterministic
stand-in lets the suite run offline. Point `ask()` at OpenAI, Anthropic,
Ollama or your internal endpoint and the same tests apply.
"""


def ask(question: str) -> dict:
    """Return a fake RAG-style answer for the given question."""
    if "refund" in question.lower():
        return {
            "answer": "Refunds for international roaming are available within 30 days of purchase.",
            "citations": ["https://help.example.com/refund-policy"],
        }
    if "password" in question.lower():
        return {
            "answer": "Open settings, choose security, and follow the reset link sent to your email.",
            "citations": ["https://help.example.com/password-reset"],
        }
    return {
        "answer": "I cannot help with that request.",
        "citations": [],
    }
