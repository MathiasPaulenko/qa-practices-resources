"""Executable subset of the article's hallucination-detection cases."""

import pytest

from claim_verifier import Report, Verdict, extract_claims, verify, verify_claim


# --- pipeline basics ---------------------------------------------------------

def test_extract_claims_splits_atomic_sentences():
    out = "The deadline is Friday. The meeting starts at noon!"
    assert extract_claims(out) == ["The deadline is Friday.", "The meeting starts at noon!"]


def test_fully_supported_answer_ships():
    out = "The deadline is Friday. The meeting starts at noon."
    src = ["The deadline is Friday, and the meeting starts at noon."]
    report = verify(out, src)
    assert report.score == 1.0
    assert report.decision == "ship"


def test_partial_support_goes_to_review():
    out = "The deadline is Friday. The meeting starts at noon. The budget was approved."
    src = ["The deadline is Friday, and the meeting starts at noon."]
    report = verify(out, src)
    assert report.decision == "review"
    assert len(report.unsupported) == 1


# --- article cases -----------------------------------------------------------

def test_tc01_nonexistent_person_is_unsupported():
    cv = verify_claim("The CTO is Jane Doe.", ["Acme was founded in 2019 in Austin."])
    assert cv.verdict is Verdict.UNSUPPORTED


def test_tc02_nonexistent_founding_year_is_unsupported():
    cv = verify_claim("The company was founded in 2015.", ["Acme is a startup in Austin."])
    assert cv.verdict is Verdict.UNSUPPORTED


def test_tc03_unsupported_statistic_is_flagged():
    cv = verify_claim("Revenue was 5 million in 2024.", ["The report discusses hiring plans."])
    assert cv.verdict is Verdict.UNSUPPORTED


def test_tc04_post_cutoff_event_is_unsupported():
    cv = verify_claim(
        "Argentina won the 2030 World Cup.",
        ["The FIFA World Cup in 2030 is scheduled for June."],
    )
    assert cv.verdict is Verdict.UNSUPPORTED


def test_tc05_fabricated_citation_is_unsupported():
    papers = ["Smith et al. 2021: Grounding Language Models.", "Lopez 2019: Retrieval QA."]
    cv = verify_claim("Doe et al. 2020 proves this method.", papers)
    assert cv.verdict is Verdict.UNSUPPORTED


def test_tc06_numeric_contradiction_is_contradicted():
    cv = verify_claim(
        "The system supports up to 200 concurrent users.",
        ["The system supports up to 100 concurrent users."],
    )
    assert cv.verdict is Verdict.CONTRADICTED


def test_tc07_parametric_override_is_unsupported():
    cv = verify_claim(
        "CheckoutLib also accepts GET requests.",
        ["CheckoutLib accepts POST only."],
    )
    assert cv.verdict is Verdict.UNSUPPORTED


def test_tc09_invented_list_item_is_unsupported():
    cv = verify_claim(
        "The SDK supports Python, Java and Go.",
        ["Supported languages: Python and Java."],
    )
    assert cv.verdict is Verdict.UNSUPPORTED


def test_tc10_domain_definition_uses_source_wording():
    cv = verify_claim(
        "In TaskFlow a reviewer requests approval.",
        ["In TaskFlow, a 'reviewer' is the requester, not the approver."],
    )
    assert cv.verdict is Verdict.SUPPORTED


def test_tc12_unsupported_relationship_inference():
    cv = verify_claim(
        "Company X acquired subsidiary Company Z last year.",
        ["Company X hired CEO Y, who previously worked at Company Z."],
    )
    assert cv.verdict is Verdict.UNSUPPORTED


def test_tc13_unstated_geography_is_unsupported():
    cv = verify_claim(
        "The product is available in Canada.",
        ["CheckoutLib 4.0 launches with a new plugin API."],
    )
    assert cv.verdict is Verdict.UNSUPPORTED


def test_tc16_conflicting_sources_flag_contradiction():
    cv = verify_claim(
        "The launch happened on March 5.",
        ["The launch happened on March 5.", "The launch happened on March 8."],
    )
    assert cv.verdict is Verdict.CONTRADICTED
    assert cv.conflicting_source == "The launch happened on March 8."


def test_tc17_empty_source_set_blocks_everything():
    report = verify("Any factual answer goes here.", [])
    assert report.score == 0.0
    assert report.decision == "review"
    assert all(c.verdict is Verdict.UNSUPPORTED for c in report.claims)


def test_tc18_minimal_context_cannot_support_inference():
    cv = verify_claim(
        "Revenue grew because the new pricing tier attracted enterprise clients.",
        ["Revenue grew 12 percent."],
    )
    assert cv.verdict is not Verdict.SUPPORTED
