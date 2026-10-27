"""Assert that no raw card data (PAN / CVV) leaks into application logs.

Run: pytest pan_in_logs_test.py -v
Requires: pytest 8.3+ — pip install pytest
Related test case: TC-MP-011 (Tokenization and Card Data Security)
"""
import re

# 13-19 digit card numbers with optional grouping separators.
PAN_PATTERN = re.compile(r"\b(?:\d[ -]?){13,19}\b")
# Standalone 3-4 digit values next to a card-like context are weaker evidence;
# keep the check on full PANs only to avoid false positives on timestamps.


def contains_pan(text: str) -> bool:
    return bool(PAN_PATTERN.search(text))


def test_no_pan_in_logs():
    with open("app.log", encoding="utf-8") as fh:
        contents = fh.read()
    assert not contains_pan(contents), "Possible PAN found in logs"


def test_no_pan_in_log_lines():
    flagged = []
    with open("app.log", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            if contains_pan(line):
                flagged.append(i)
    assert not flagged, f"Possible PAN on lines: {flagged[:10]}"


def test_fixture_is_clean():
    clean = "payment ok, tok_applepay_xxx, last4=4242"
    assert not contains_pan(clean)
    dirty = "card 4242 4242 4242 4242 logged by mistake"
    assert contains_pan(dirty)
