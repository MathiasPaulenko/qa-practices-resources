"""Minimal rule-based moderation filter used by the test suite.

``moderate(text)`` mimics what a real pipeline does before a match:
NFKC normalization, common homoglyph mapping, leet-speak folding,
emoji/punctuation stripping, then word-boundary matching against a
small blocklist. Toxicity is a toy scorer: keyword hits produce a
deterministic score so threshold behavior can be tested exactly at
the boundary.
"""

import re
import unicodedata
from dataclasses import dataclass

BLOCKLIST = {"shit", "fuck", "damn"}
TOXIC_TERMS = {"kill", "hate", "idiot", "stupid"}

LEET = str.maketrans({"1": "i", "3": "e", "4": "a", "0": "o", "5": "s", "7": "t", "*": "u"})
HOMOGLYPHS = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x",
    "і": "i", "ј": "j", "һ": "h", "ѕ": "s", "у": "y", "ν": "v",
    "ο": "o", "α": "a",
})
_EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F02F\uFE0F]",
)


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(HOMOGLYPHS).translate(LEET)
    text = _EMOJI_RE.sub(" ", text)
    return text.lower()


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z]+", _normalize(text))


def _has_profanity(words: list[str]) -> bool:
    """Exact token match, or an exact concatenation of contiguous tokens.

    ``s h i t`` and ``s.hit`` tokenize to parts that rejoin to a blocklist
    word; ``is hit`` must not match ``shit`` because ``is`` is a whole token.
    """
    for w in BLOCKLIST:
        if w in words:
            return True
        for start in range(len(words)):
            joined = ""
            for end in range(start, len(words)):
                joined += words[end]
                if joined == w:
                    return True
                if len(joined) >= len(w):
                    break
    return False


@dataclass
class ModerationResult:
    score: float
    action: str  # "allow" | "flag" | "block"
    flags: list[str]


def moderate(text: str, threshold: float = 0.5) -> ModerationResult:
    flags: list[str] = []

    if text.strip() == "":
        return ModerationResult(score=0.0, action="allow", flags=[])

    if len(re.findall(r"https?://", text)) >= 5:
        flags.append("excessive_links")

    words = _tokens(text)
    if _has_profanity(words):
        flags.append("profanity")

    toxic_hits = sum(1 for w in words if w in TOXIC_TERMS)
    score = 1.0 if "profanity" in flags else (min(0.2 + 0.6 * toxic_hits, 1.0) if toxic_hits else 0.1)

    if score >= 0.8 or ("profanity" in flags and score > threshold):
        action = "block" if score >= 0.8 else "flag"
    elif flags or score > threshold:
        action = "flag"
    else:
        action = "allow"

    return ModerationResult(score=score, action=action, flags=flags)
