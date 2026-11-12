"""Layer 1 — schema / contract gate. Requires: pytest, jsonschema."""

import jsonschema

from support_bot import ask


def test_refund_answer_has_citations():
    answer = ask("Can I get a refund for international roaming?")
    schema = {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "citations": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["answer", "citations"],
    }
    jsonschema.validate(answer, schema)
    assert len(answer["citations"]) > 0


def test_unknown_question_still_returns_contract():
    """Even refusals must satisfy the response contract."""
    answer = ask("What is the airspeed of an unladen swallow?")
    schema = {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "citations": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["answer", "citations"],
    }
    jsonschema.validate(answer, schema)
