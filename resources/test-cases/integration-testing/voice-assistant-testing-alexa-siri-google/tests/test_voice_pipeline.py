"""Executable subset of the voice assistant test cases.

Each test maps to a TC on qapractices.com/test-cases/
voice-assistant-testing-alexa-siri-google. The simulator stands in
for the real device chain so the properties (wake thresholds,
degradation budgets, fallback limits) are asserted deterministically.
"""

import pytest

from voice_pipeline_simulator import VoicePipeline


@pytest.fixture
def pipeline():
    return VoicePipeline()


# TC-01: wake word detection rate
def test_wake_word_threshold(pipeline):
    assert pipeline.hear("add milk to my list", wake_confidence=0.9).heard
    assert not pipeline.hear("add milk to my list", wake_confidence=0.4).heard


def test_near_homophone_does_not_wake(pipeline):
    # Low-confidence "wake word" events (TV dialogue, homophones) stay asleep.
    assert not pipeline.hear("alexis", wake_confidence=0.3).heard
    assert pipeline.history == []  # nothing was recorded either — TC-07 property


# TC-02: intent recognition accuracy
@pytest.mark.parametrize("utterance,expected_item", [
    ("add milk to my list", "milk"),           # training phrase
    ("put milk on the list", "milk"),          # paraphrase
    ("put oat milk on the list", "oat milk"),  # paraphrase, multiword slot
    ("i need milk", "milk"),                   # loose phrasing
])
def test_paraphrases_resolve_to_add_item(pipeline, utterance, expected_item):
    turn = pipeline.hear(utterance)
    assert turn.intent == "AddItemIntent"
    assert turn.slots["item"] == expected_item


def test_out_of_domain_utterance_falls_back(pipeline):
    turn = pipeline.hear("blorptastic banana rocket")
    assert turn.intent is None
    assert "didn't get that" in turn.reply


# TC-03: slot filling and entity extraction
def test_bare_intent_triggers_slot_elicitation(pipeline):
    turn = pipeline.hear("add something to my list")
    assert "what should I add" in turn.reply  # elicits the missing slot


def test_slot_per_turn_dialog_fills_each_slot(pipeline):
    pipeline.hear("book a flight")
    turn = pipeline.hear("lisbon")
    assert turn.slots["destination"] == "lisbon"
    turn = pipeline.hear("next friday")
    assert turn.slots["date"] == "next friday"


def test_multiword_slot_captured_verbatim(pipeline):
    turn = pipeline.hear("add oat milk to my shopping list")
    assert turn.slots["item"] == "oat milk"


# TC-04: multi-turn conversation and mid-dialog correction
def test_context_survives_and_correction_replaces_slot(pipeline):
    pipeline.hear("book a flight")
    pipeline.hear("lisbon")
    pipeline.hear("next friday")
    turn = pipeline.hear("actually change destination to porto")
    assert turn.slots["destination"] == "porto"
    assert turn.slots["date"] == "next friday"  # stale value untouched


# TC-05: error handling and fallbacks
def test_fallback_exits_after_limit(pipeline):
    pipeline.hear("gibberish one")
    pipeline.hear("gibberish two")
    turn = pipeline.hear("gibberish three")
    assert turn.end_session
    assert "goodbye" in turn.reply


def test_backend_timeout_returns_friendly_message():
    def slow_backend(intent, slots):
        raise TimeoutError("10s exceeded")

    pipe = VoicePipeline(fulfillment=slow_backend)
    turn = pipe.hear("add milk to my list")
    assert "didn't respond" in turn.reply
    assert not turn.end_session  # session survives — user can retry


# TC-06 + TC-09: accents and noise degrade gracefully, never a cliff
def test_noise_budget_is_gradual(pipeline):
    quiet = pipeline.hear("add milk to my list", noise_db=40)
    moderate = VoicePipeline().hear("add milk to my list", noise_db=65)
    loud = VoicePipeline().hear("add milk to my list", noise_db=75)
    assert quiet.intent == "AddItemIntent"
    # 65 dB drops words but the key phrase fragment may still parse or
    # fall back — either way the turn is *handled*, not silently lost.
    assert moderate.heard and moderate.reply
    # 75 dB: degradation produces a transcript the NLU cannot map → fallback.
    assert loud.heard
    assert loud.intent is None or loud.intent == "AddItemIntent"


def test_accented_speaker_still_parses():
    pipe = VoicePipeline()
    turn = pipe.hear("add milk to my list", speaker="accented")
    # 15% drop may lose a word; the pipeline still responds, never crashes.
    assert turn.heard and turn.reply


# TC-07: privacy — only woken interactions are recorded, deletion works
def test_unwoken_audio_leaves_no_history(pipeline):
    pipeline.hear("private conversation", wake_confidence=0.2)
    assert pipeline.history == []


def test_delete_what_i_just_said(pipeline):
    pipeline.hear("add milk to my list")
    pipeline.hear("what's on my list")
    assert len(pipeline.history) == 2
    pipeline.delete_last()
    assert len(pipeline.history) == 1
    assert pipeline.history[0]["intent"] == "AddItemIntent"


# TC-10: type-to-text input is equivalent to voice
def test_text_input_matches_voice_result(pipeline):
    voice = pipeline.hear("add milk to my list")
    text = pipeline.hear_text("add milk to my list")
    assert voice.intent == text.intent == "AddItemIntent"
    assert voice.slots == text.slots
    assert text.card  # visual alternative exists for hearing-impaired users
