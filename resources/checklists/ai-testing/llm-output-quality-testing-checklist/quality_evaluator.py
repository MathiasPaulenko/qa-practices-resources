"""Deterministic offline scorer for LLM output quality.

Each scorer maps to one dimension of the output-quality checklist so a
failing case points to a specific section instead of a vague "low quality".
"""

from __future__ import annotations

import re
from typing import Iterable


_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "before", "but", "by",
    "can", "for", "from", "if", "in", "is", "it", "its", "of", "on",
    "or", "so", "that", "the", "to", "when", "while", "with", "your",
}


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9áéíóúñü]+", text.lower())
    return {w for w in words if w not in _STOPWORDS}


def _token_similarity(a: str, b: str) -> float:
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return 2 * len(ta & tb) / (len(ta) + len(tb))


def consistency_score(answers: list[str]) -> float:
    """Average pairwise token overlap across repeated answers to one prompt.

    Token-based so valid paraphrases score high while a model answering a
    different question each run scores low.
    """
    if len(answers) < 2:
        return 1.0
    pairs = [
        _token_similarity(a, b)
        for i, a in enumerate(answers)
        for b in answers[i + 1 :]
    ]
    return sum(pairs) / len(pairs)


def grounding_score(answer: str, reference_facts: Iterable[str]) -> float:
    """Share of required facts present in the answer (case-insensitive)."""
    facts = list(reference_facts)
    if not facts:
        return 1.0
    low = answer.lower()
    hits = sum(1 for f in facts if f.lower() in low)
    return hits / len(facts)


def contradiction_score(answer: str) -> float:
    """Flag answers that state and deny the same claim in one response."""
    lowered = answer.lower()
    denial_patterns = (
        r"\bhowever,?\s+(it is|this is)\s+not\b",
        r"\bbut\s+(in fact|actually)\b.*\bnot\b",
    )
    for pattern in denial_patterns:
        if re.search(pattern, lowered):
            return 0.0
    return 1.0


def relevance_score(answer: str, required_terms: Iterable[str]) -> float:
    """Share of terms the user asked about that appear in the answer."""
    terms = list(required_terms)
    if not terms:
        return 1.0
    low = answer.lower()
    hits = sum(1 for t in terms if t.lower() in low)
    return hits / len(terms)


def refusal_detected(answer: str) -> bool:
    """Detect a refusal that redirects instead of just blocking."""
    refusal_markers = ("can't", "cannot", "unable to", "not able to")
    redirect_markers = ("instead", "use ", "contact", "reset", "alternatively")
    low = answer.lower()
    return any(m in low for m in refusal_markers) and any(
        m in low for m in redirect_markers
    )


def evaluate_case(case: dict, answers: list[str]) -> dict:
    """Score one eval case against its sampled answers."""
    scores: dict[str, float] = {"consistency": consistency_score(answers)}
    for answer in answers:
        if "reference_facts" in case:
            scores["grounding"] = grounding_score(
                answer, case["reference_facts"]
            )
        scores["contradiction"] = contradiction_score(answer)
        if "required_terms" in case:
            scores["relevance"] = relevance_score(
                answer, case["required_terms"]
            )
    if case.get("refusal_expected"):
        scores["refusal"] = 1.0 if all(refusal_detected(a) for a in answers) else 0.0
    passed = scores["consistency"] >= case.get("min_similarity", 0.0) and all(
        v >= 0.5 for k, v in scores.items() if k != "consistency"
    )
    return {"id": case["id"], "dimension": case["dimension"],
            "scores": scores, "passed": passed}
