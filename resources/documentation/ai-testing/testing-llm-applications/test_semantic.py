"""Layer 2 — semantic similarity floor.

Requires: pytest, sentence-transformers, numpy.
Model all-MiniLM-L6-v2 downloads once (~90MB) on first run.
"""

import numpy as np
import pytest
from sentence_transformers import SentenceTransformer

from support_bot import ask

model = SentenceTransformer("all-MiniLM-L6-v2")


def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def test_answer_matches_expected_meaning():
    expected = (
        "Refunds for international roaming are available within 30 days of purchase."
    )
    actual = ask("Can I get a refund for international roaming?")["answer"]
    sim = cosine(*model.encode([expected, actual]))
    assert sim >= 0.70, f"semantic similarity {sim:.2f} below floor"


@pytest.mark.xfail(reason="intentional mismatch — shows the floor catching drift")
def test_wrong_meaning_fails_the_floor():
    expected = "Refunds for international roaming are available within 30 days of purchase."
    actual = "Your account balance is due on the first of next month."
    sim = cosine(*model.encode([expected, actual]))
    assert sim >= 0.70, f"semantic similarity {sim:.2f} below floor"
