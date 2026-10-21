"""Stdlib model of the claim-level hallucination-detection pipeline.

Mirrors the article's pipeline: split the generated answer into atomic
claims, check each claim against the retrieved sources, then score
supported/total to decide ship vs. human review. Token-overlap scoring
stands in for the embedding/NLI calls so the suite runs fully offline.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum

WORD_RE = re.compile(r"[a-záéíóúüñ0-9]+")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")

SUPPORT_THRESHOLD = 0.75  # token coverage needed to call a claim supported
SHIP_THRESHOLD = 0.95     # supported/total needed to ship without review


class Verdict(str, Enum):
    SUPPORTED = "supported"
    UNSUPPORTED = "unsupported"
    CONTRADICTED = "contradicted"


@dataclass
class ClaimVerdict:
    claim: str
    verdict: Verdict
    coverage: float
    conflicting_source: str | None = None


@dataclass
class Report:
    score: float
    decision: str  # "ship" | "review"
    claims: list[ClaimVerdict] = field(default_factory=list)

    @property
    def unsupported(self) -> list[ClaimVerdict]:
        return [c for c in self.claims if c.verdict is not Verdict.SUPPORTED]


def extract_claims(text: str) -> list[str]:
    """Split generated output into atomic sentences."""
    return [s.strip() for s in SENTENCE_SPLIT.split(text) if s.strip()]


def _tokens(text: str) -> set[str]:
    return set(WORD_RE.findall(text.lower()))


def _numbers(text: str) -> set[str]:
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def _match(tok: str, src: set[str]) -> bool:
    """Loose match: equal, or prefix-shared morphology (request/requests/requester)."""
    if tok in src:
        return True
    return any(t[:6] == tok[:6] for t in src if len(t) >= 6 and len(tok) >= 6)


def _coverage(claim: str, source: str) -> float:
    ct = _tokens(claim) - _numbers(claim)
    if not ct:
        return 0.0
    st = _tokens(source)
    return sum(1 for t in ct if _match(t, st)) / len(ct)


def _source_verdict(claim: str, source: str) -> Verdict:
    cov = _coverage(claim, source)
    claim_nums = _numbers(claim)
    if claim_nums and cov >= 0.5:
        src_nums = _numbers(source)
        if src_nums and not claim_nums <= src_nums:
            return Verdict.CONTRADICTED
    if cov >= SUPPORT_THRESHOLD:
        return Verdict.SUPPORTED
    return Verdict.UNSUPPORTED


def verify_claim(claim: str, sources: list[str]) -> ClaimVerdict:
    if not sources:
        return ClaimVerdict(claim, Verdict.UNSUPPORTED, 0.0)
    verdicts = [(s, _source_verdict(claim, s)) for s in sources]
    cov = max(_coverage(claim, s) for s in sources)
    supported = [s for s, v in verdicts if v is Verdict.SUPPORTED]
    contradicted = [s for s, v in verdicts if v is Verdict.CONTRADICTED]
    if contradicted:
        return ClaimVerdict(claim, Verdict.CONTRADICTED, cov, contradicted[0])
    if supported:
        return ClaimVerdict(claim, Verdict.SUPPORTED, cov)
    return ClaimVerdict(claim, Verdict.UNSUPPORTED, cov)


def verify(output: str, sources: list[str], ship_threshold: float = SHIP_THRESHOLD) -> Report:
    """Run the pipeline: claims -> per-claim verdicts -> ship/review decision."""
    claims = [verify_claim(c, sources) for c in extract_claims(output)]
    score = sum(c.verdict is Verdict.SUPPORTED for c in claims) / len(claims) if claims else 0.0
    return Report(score=score, decision="ship" if score >= ship_threshold else "review", claims=claims)
