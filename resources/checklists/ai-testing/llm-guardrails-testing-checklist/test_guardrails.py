"""Offline suite: run the adversarial dataset against the mock pipeline."""
import json
from pathlib import Path

import pytest

from guarded_pipeline import guarded_chat

PROMPTS = json.loads(
    (Path(__file__).parent / "adversarial_prompts.json").read_text(encoding="utf-8")
)


@pytest.mark.parametrize("case", PROMPTS, ids=[c["id"] for c in PROMPTS])
def test_guardrail_decision(case):
    result = guarded_chat(case["prompt"])
    assert result["blocked"] == case["expect_blocked"], (
        f"{case['id']} ({case['category']}): expected blocked={case['expect_blocked']}, "
        f"got {result['blocked']} at stage '{result['stage']}'"
    )
