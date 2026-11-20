"""Minimal guarded LLM pipeline for offline testing.

Implements the policies from guardrails_config.json in front of a canned
"model" so the adversarial suite can run without a live endpoint.
"""
import json
import re
from pathlib import Path

CONFIG = json.loads(
    (Path(__file__).parent / "guardrails_config.json").read_text(encoding="utf-8")
)


def _regex_policies() -> list[re.Pattern]:
    patterns = []
    for policy in CONFIG["policies"]:
        if policy["type"] == "regex":
            patterns.extend(re.compile(p) for p in policy["patterns"])
    return patterns


def _keyword_policies() -> list[str]:
    patterns = []
    for policy in CONFIG["policies"]:
        if policy["type"] == "keyword":
            patterns.extend(p.lower() for p in policy["patterns"])
    return patterns


REGEX_RULES = _regex_policies()
KEYWORD_RULES = _keyword_policies()

SAFE_REPLY = "I can't help with that request."


def guarded_chat(prompt: str) -> dict:
    """Simulates: sanitize -> injection check -> model -> PII filter -> reply."""
    lowered = prompt.lower()

    # Input guardrail: keyword-based injection filter.
    if any(k in lowered for k in KEYWORD_RULES):
        return {"answer": SAFE_REPLY, "blocked": True, "stage": "input"}

    # Canned model: echoes the prompt when asked to repeat secrets.
    if "repeat" in lowered or "echo" in lowered:
        answer = f"You said: {prompt}"
    else:
        answer = "This is a safe, on-topic response from the mock model."

    # Output guardrail: PII must not leave in the answer.
    for rule in REGEX_RULES:
        if rule.search(answer):
            return {"answer": SAFE_REPLY, "blocked": True, "stage": "output"}

    return {"answer": answer, "blocked": False, "stage": "none"}
