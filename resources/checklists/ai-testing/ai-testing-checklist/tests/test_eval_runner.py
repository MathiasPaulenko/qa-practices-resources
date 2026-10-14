"""Offline tests for eval_runner — the MockClient supplies every answer."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from eval_runner import evaluate_llm, run_dataset
from mock_llm import MockClient

DATASET = os.path.join(os.path.dirname(__file__), "..", "guardrail_dataset.json")


def make_client(text):
    return MockClient({"any prompt": text})


def test_passes_when_expected_present_and_forbidden_absent():
    client = make_client("the refund window is 30 days")
    result = evaluate_llm("any prompt", ["refund", "days"], ["transfer"], client=client)
    assert result == "the refund window is 30 days"


def test_fails_when_expected_content_missing():
    client = make_client("the answer mentions nothing relevant")
    with pytest.raises(AssertionError, match="Missing expected content"):
        evaluate_llm("any prompt", ["refund"], [], client=client)


def test_fails_when_forbidden_content_present():
    client = make_client("you can transfer the funds to your personal account")
    with pytest.raises(AssertionError, match="Forbidden content"):
        evaluate_llm("any prompt", ["transfer"], ["personal account"], client=client)


def test_matching_is_case_insensitive():
    client = make_client("REFUND requests take 30 DAYS")
    result = evaluate_llm("any prompt", ["refund", "days"], [], client=client)
    assert result.startswith("refund")


def test_run_dataset_marks_pass_and_fail():
    client = MockClient()  # built-in responses satisfy all three cases
    results = run_dataset(DATASET, client=client)
    assert len(results) == 3
    assert all(ok for _, ok in results)


def test_run_dataset_reports_failure_without_raising():
    client = MockClient({"How do I reset my password?": "I cannot help with that."})
    results = run_dataset(DATASET, client=client)
    failed = [text for text, ok in results if not ok]
    assert failed == ["How do I reset my password?"]
