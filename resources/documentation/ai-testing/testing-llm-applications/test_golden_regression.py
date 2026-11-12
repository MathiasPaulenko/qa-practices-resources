"""Layer 4 — golden dataset regression. Requires: pytest."""

import json
from pathlib import Path

import pytest

from support_bot import ask

GOLDEN_FILE = Path(__file__).parent / "golden_dataset.jsonl"
GOLDEN = [json.loads(line) for line in GOLDEN_FILE.read_text().splitlines()]


@pytest.mark.parametrize("case", GOLDEN)
def test_golden_answer_still_holds(case):
    answer = ask(case["question"])["answer"].lower()
    for keyword in case["must_contain"]:
        assert keyword in answer, f"'{case['question']}' lost '{keyword}'"
