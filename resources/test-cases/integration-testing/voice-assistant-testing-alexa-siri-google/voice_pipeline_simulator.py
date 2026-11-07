"""Deterministic model of a voice assistant request pipeline.

Mirrors the stages in the qapractices.com test cases:
    wake word -> ASR -> NLU (intent + slots) -> dialog -> response

Every stage is deterministic — no model calls, no randomness without a
seed — so the pytest suite can assert the properties the article's
test cases describe (wake thresholds, graceful degradation, fallback
limits, mid-dialog corrections, history recording) fully offline.
"""

from __future__ import annotations

from dataclasses import dataclass, field

FALLBACK_LIMIT = 2  # third unclear input ends the session politely

# How many words the ASR "drops" per condition, as a fraction.
SPEAKER_DEGRADATION = {"native": 0.0, "accented": 0.15, "dialect": 0.30}


@dataclass
class Turn:
    heard: bool
    transcript: str | None = None
    intent: str | None = None
    slots: dict = field(default_factory=dict)
    reply: str = ""
    end_session: bool = False
    card: str | None = None  # visual payload for screen devices


class WakeWordEngine:
    """Wakes only when the sample's confidence clears the threshold."""

    def __init__(self, threshold: float = 0.7) -> None:
        self.threshold = threshold

    def wakes(self, confidence: float) -> bool:
        return confidence >= self.threshold


class ASR:
    """Speech-to-text with deterministic word dropping.

    Drop probability comes from the noisiest applicable condition
    (room noise or speaker profile). Words are removed at fixed
    positions so the same input always degrades the same way —
    that's what makes regressions attributable in a real suite.
    """

    def transcribe(self, utterance: str, noise_db: float, speaker: str) -> str:
        drop = SPEAKER_DEGRADATION.get(speaker, 0.0)
        if noise_db >= 70:
            drop = max(drop, 0.35)
        elif noise_db >= 50:
            drop = max(drop, 0.15)
        if drop == 0.0:
            return utterance
        every = max(2, round(1 / drop))
        words = [w for i, w in enumerate(utterance.split()) if i % every != 0]
        return " ".join(words)


class NLU:
    """Intent + slot lookup over a phrase table.

    A real model assigns probabilities; this fixture stands in for
    the trained interaction model. Paraphrases map to the same intent
    as the training phrase — the property under test in TC-02.
    """

    PHRASE_TABLE = {
        "add milk to my list": ("AddItemIntent", {"item": "milk"}),
        "put milk on the list": ("AddItemIntent", {"item": "milk"}),
        "put oat milk on the list": ("AddItemIntent", {"item": "oat milk"}),
        "add oat milk to my shopping list": ("AddItemIntent", {"item": "oat milk"}),
        "add something to my list": ("AddItemIntent", {}),
        "i need milk": ("AddItemIntent", {"item": "milk"}),
        "what's on my list": ("GetListIntent", {}),
        "book a flight": ("BookFlightIntent", {}),
        "actually change destination to porto": ("CorrectSlotIntent", {"destination": "porto"}),
    }
    REQUIRED_SLOTS = {"AddItemIntent": ["item"], "BookFlightIntent": ["destination", "date"]}
    SLOT_ANSWERS = {"lisbon": ("destination", "lisbon"), "next friday": ("date", "next friday")}

    def parse(self, transcript: str) -> tuple[str | None, dict]:
        key = transcript.lower().strip()
        if key in self.PHRASE_TABLE:
            intent, slots = self.PHRASE_TABLE[key]
            return intent, dict(slots)
        if key in self.SLOT_ANSWERS:
            slot, value = self.SLOT_ANSWERS[key]
            return "ProvideSlotIntent", {slot: value}
        return None, {}


class DialogManager:
    """Keeps session state: pending slots, fallback count, corrections."""

    def __init__(self, items: list[str] | None = None) -> None:
        self.slots: dict = {}
        self.pending_intent: str | None = None
        self.fallback_count = 0
        self.items = items if items is not None else ["eggs"]

    def handle(self, intent: str | None, slots: dict, transcript: str | None) -> Turn:
        if intent is None:
            return self._fallback(transcript)
        if intent == "ProvideSlotIntent":
            self.slots.update(slots)
            return self._continue_pending(transcript)
        if intent == "CorrectSlotIntent":
            self.slots.update(slots)
            return Turn(True, transcript, intent, dict(self.slots),
                        reply=f"OK, destination changed to {slots['destination']}.")
        self.fallback_count = 0
        missing = [s for s in NLU.REQUIRED_SLOTS.get(intent, []) if s not in slots and s not in self.slots]
        if missing:
            self.pending_intent = intent
            return Turn(True, transcript, intent, dict(self.slots),
                        reply=f"Sure — {self._elicit(missing[0])}?")
        return self._fulfill(intent, slots, transcript)

    def _continue_pending(self, transcript: str | None) -> Turn:
        intent = self.pending_intent or "AddItemIntent"
        missing = [s for s in NLU.REQUIRED_SLOTS.get(intent, []) if s not in self.slots]
        if missing:
            return Turn(True, transcript, intent, dict(self.slots),
                        reply=f"Sure — {self._elicit(missing[0])}?")
        self.pending_intent = None
        return self._fulfill(intent, {}, transcript)

    def _fulfill(self, intent: str, slots: dict, transcript: str | None) -> Turn:
        merged = {**self.slots, **slots}
        if intent == "AddItemIntent":
            item = merged["item"]
            self.items.append(item)
            self.slots.clear()
            return Turn(True, transcript, intent, merged,
                        reply=f"OK, I added {item} to your list.",
                        card=f"Shopping list ({len(self.items)} items): {', '.join(self.items)}")
        if intent == "GetListIntent":
            return Turn(True, transcript, intent, merged,
                        reply=f"Your list has {', '.join(self.items)}.")
        if intent == "BookFlightIntent":
            self.slots.update(merged)
            return Turn(True, transcript, intent, dict(self.slots),
                        reply="Booking your flight.")
        return Turn(True, transcript, intent, merged, reply="Done.")

    def _fallback(self, transcript: str | None) -> Turn:
        self.fallback_count += 1
        if self.fallback_count > FALLBACK_LIMIT:
            return Turn(True, transcript, end_session=True,
                        reply="I'm still having trouble. Try again later — goodbye.")
        return Turn(True, transcript, reply="Sorry, I didn't get that. Could you say it another way?")

    @staticmethod
    def _elicit(slot: str) -> str:
        return {"item": "what should I add", "destination": "where to", "date": "when"}.get(slot, slot)


class VoicePipeline:
    """wake word -> ASR -> NLU -> dialog -> response, plus voice history."""

    def __init__(self, fulfillment=None, wake_threshold: float = 0.7) -> None:
        self.wake = WakeWordEngine(wake_threshold)
        self.asr = ASR()
        self.nlu = NLU()
        self.dialog = DialogManager()
        self.fulfillment = fulfillment  # optional callable(intent, slots); may raise TimeoutError
        self.history: list[dict] = []

    def hear(self, utterance: str, wake_confidence: float = 1.0,
             noise_db: float = 40, speaker: str = "native") -> Turn:
        if not self.wake.wakes(wake_confidence):
            return Turn(heard=False)
        transcript = self.asr.transcribe(utterance, noise_db, speaker)
        return self._route(transcript)

    def hear_text(self, utterance: str) -> Turn:
        """Type-to-text input: skips acoustics, same NLU and dialog."""
        return self._route(utterance)

    def _route(self, transcript: str) -> Turn:
        intent, slots = self.nlu.parse(transcript)
        if intent and self.fulfillment:
            try:
                self.fulfillment(intent, slots)
            except TimeoutError:
                turn = Turn(True, transcript, intent, slots,
                            reply="The service didn't respond. Want me to try again?")
                self._record(turn)
                return turn
        turn = self.dialog.handle(intent, slots, transcript)
        self._record(turn)
        return turn

    def _record(self, turn: Turn) -> None:
        self.history.append({"transcript": turn.transcript, "intent": turn.intent})

    def delete_last(self) -> None:
        """'Delete what I just said.'"""
        if self.history:
            self.history.pop()
