"""Tests for the reference moderation filter (mirrors the site's test cases)."""

import pytest

from conftest import moderate


# --- Positive cases -------------------------------------------------------

def test_detect_profanity_in_text():
    r = moderate("This is shit")
    assert "profanity" in r.flags
    assert r.action == "block"


def test_allow_clean_content():
    r = moderate("Great product, fast shipping!")
    assert r.action == "allow"
    assert r.flags == []


def test_spam_detection_repeated_links():
    text = " ".join(["http://deals.example"] * 5)
    r = moderate(text)
    assert "excessive_links" in r.flags
    assert r.action == "flag"


def test_high_toxicity_scores_high():
    r = moderate("i hate you stupid idiot")
    assert r.score > 0.8
    assert r.action == "block"


def test_low_toxicity_scores_low():
    r = moderate("I disagree with the approach")
    assert r.score < 0.3
    assert r.action == "allow"


# --- False positives (the Scunthorpe problem) -----------------------------

SCUNTHORPE_TERMS = ["scunthorpe", "analysis", "hellp syndrome", "assassin", "class"]


@pytest.mark.parametrize("term", SCUNTHORPE_TERMS)
def test_dictionary_and_medical_terms_not_flagged(term):
    assert moderate(term).action != "block", f"{term} incorrectly blocked"


def test_legitimate_sensitive_discussion_allowed():
    r = moderate("The historical context of violence in the region")
    assert r.action in ("allow", "flag")
    assert r.score < 0.8


# --- Bypass attempts ------------------------------------------------------

@pytest.mark.parametrize("variant", ["sh1t", "s h i t", "s.h.i.t"])
def test_leet_and_spacing_bypass_detected(variant):
    r = moderate(f"you {variant} me")
    assert "profanity" in r.flags


def test_unicode_homoglyph_bypass_detected():
    r = moderate("ѕhit")  # Cyrillic ѕ (U+0455) -> NFKC/normalize must catch it
    assert "profanity" in r.flags


def test_emoji_insertion_bypass_detected():
    r = moderate("s🚫hit")
    assert "profanity" in r.flags


def test_unicode_normalization_equivalence():
    nfc = moderate("café")          # NFC
    nfd = moderate("café")         # NFD (e + combining acute)
    assert nfc.action == nfd.action
    assert nfc.score == nfd.score


# --- Boundaries and edges -------------------------------------------------

def test_toxicity_exactly_at_threshold_is_deterministic():
    # Rule: score >= threshold blocks. "idiot" scores exactly 0.8.
    r1 = moderate("idiot", threshold=0.8)
    r2 = moderate("idiot", threshold=0.8)
    assert r1.score == 0.8
    assert r1.action == r2.action == "block"


def test_score_above_threshold_flags():
    r = moderate("kill idiot", threshold=0.8)   # 0.2 + 1.2 -> capped 1.0 > 0.8
    assert r.action == "block"


@pytest.mark.parametrize("text", ["", "   ", " \n\t  "])
def test_empty_and_whitespace_input(text):
    r = moderate(text)
    assert r.action == "allow"
    assert r.score == 0.0


def test_very_long_content_processed():
    text = ("nice words " * 4000) + " shit " + ("more nice " * 4000)
    r = moderate(text)
    assert "profanity" in r.flags


def test_four_links_do_not_flag():
    text = " ".join(["http://a.example"] * 4)
    assert "excessive_links" not in moderate(text).flags
