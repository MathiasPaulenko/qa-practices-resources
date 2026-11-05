import jsonschema
from qa_assistant import ask_support_bot


def test_refund_policy_answer_has_citations():
    question = "Can I get a refund for international roaming?"
    answer = ask_support_bot(question)

    schema = {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "citations": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["answer", "citations"],
    }
    jsonschema.validate(answer, schema)
    assert "policy" in answer["answer"].lower() or "plan" in answer["answer"].lower()
    assert len(answer["citations"]) > 0
