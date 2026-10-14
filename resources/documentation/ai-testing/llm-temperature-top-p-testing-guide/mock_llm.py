"""Deterministic mock LLM client simulating temperature/top-p sampling.

Mirrors the OpenAI chat.completions interface closely enough for
sweep.py and the pytest suite to run offline. A seeded RNG drives
variation: temperature controls how deep into the phrasing pool the
sampler can reach, top_p truncates the pool itself. temperature=0
always returns the top variant, like argmax decoding.
"""

import random

VARIANTS = [
    "Flaky tests make CI results unreliable and erode team trust.",
    "When tests fail unpredictably, developers stop trusting CI.",
    "Flaky tests erode confidence in CI by producing random failures.",
    "Unreliable test results undermine trust in the CI pipeline.",
    "CI loses credibility when flaky tests fail at random.",
    "Random test failures make teams doubt the whole CI suite.",
    "Flaky tests destroy trust in continuous integration pipelines.",
    "Teams start ignoring CI when flaky tests cry wolf too often.",
    "Intermittent test failures corrode confidence in CI.",
    "Untrustworthy CI results come from flaky, random test failures.",
]


class _Message:
    def __init__(self, content):
        self.content = content


class _Choice:
    def __init__(self, content):
        self.message = _Message(content)


class _Completion:
    def __init__(self, content):
        self.choices = [_Choice(content)]


class _Completions:
    def __init__(self, rng):
        self._rng = rng

    def create(self, model, messages, temperature=1.0, top_p=1.0, max_tokens=100, **kwargs):
        if temperature <= 0:
            return _Completion(VARIANTS[0])
        pool_size = max(1, round(len(VARIANTS) * min(top_p, 1.0)))
        depth = max(1, round(pool_size * temperature))
        idx = self._rng.randrange(min(depth, len(VARIANTS)))
        return _Completion(VARIANTS[idx])


class _Chat:
    def __init__(self, rng):
        self.completions = _Completions(rng)


class MockClient:
    """OpenAI-shaped client whose sampling depends on temperature and top_p."""

    def __init__(self, seed=42):
        self.chat = _Chat(random.Random(seed))
