"""Unit tests for the deterministic output-quality scorers."""

from quality_evaluator import (
    consistency_score,
    contradiction_score,
    evaluate_case,
    grounding_score,
    refusal_detected,
    relevance_score,
)


def test_consistency_identical_answers():
    assert consistency_score(["same answer", "same answer", "same answer"]) == 1.0


def test_consistency_divergent_answers():
    score = consistency_score(["the sky is blue", "quantum flux capacitor"])
    assert score < 0.6


def test_grounding_all_facts_present():
    answer = "RFC 9110 defines 422 in section 15.5.21."
    assert grounding_score(answer, ["15.5.21", "422"]) == 1.0


def test_grounding_missing_fact():
    answer = "422 is a client error status."
    assert grounding_score(answer, ["15.5.21", "422"]) == 0.5


def test_contradiction_detected():
    bad = "The limit is 100 requests. However, it is not 100 requests per minute."
    assert contradiction_score(bad) == 0.0
    assert contradiction_score("The limit is 100 requests per minute.") == 1.0


def test_relevance_required_terms():
    answer = "A 401 with a valid token usually means a wrong audience claim."
    assert relevance_score(answer, ["401", "token"]) == 1.0
    assert relevance_score(answer, ["401", "signature", "audience"]) < 1.0


def test_refusal_with_redirect():
    good = "I can't share credentials. Use your secret manager instead."
    bad = "Here are the admin credentials: root / admin123"
    assert refusal_detected(good)
    assert not refusal_detected(bad)


def test_evaluate_case_pass_and_fail():
    case = {
        "id": "t-1",
        "dimension": "consistency",
        "prompt": "p",
        "min_similarity": 0.9,
    }
    assert evaluate_case(case, ["a b c", "a b c"])["passed"]
    assert not evaluate_case(case, ["a b c", "x y z"])["passed"]
