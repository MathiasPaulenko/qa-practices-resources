"""Minimal feature-flag evaluator mirroring OpenFeature-style semantics.

Evaluation order (matches the resource diagram):
    flag exists? -> enabled (kill switch)? -> prerequisites met? ->
    explicit user rule -> segment rule -> percentage bucket -> default

Bucketing is deterministic: sha256(f"{flag_key}:{user_id}") mod 100 gives
each user a permanent bucket in 0-99, so `bucket < percentage` makes
rollouts stable and monotonic.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


@dataclass
class FlagRule:
    """Feature flag definition as stored by the flag service."""

    key: str
    enabled: bool = True
    percentage: int | None = None  # None -> boolean toggle only
    users_on: frozenset[str] = frozenset()   # explicit allow-list
    users_off: frozenset[str] = frozenset()  # explicit deny-list (wins)
    segments_on: frozenset[str] = frozenset()
    prerequisites: tuple[str, ...] = ()      # flag keys that must be on
    variants: tuple[str, ...] = ()           # A/B variants, split evenly


def bucket(flag_key: str, user_id: str) -> int:
    """Deterministic bucket in [0, 99] for a flag+user pair."""
    digest = hashlib.sha256(f"{flag_key}:{user_id}".encode()).digest()
    return int.from_bytes(digest[:4]) % 100


def evaluate(
    flag_key: str,
    flags: dict[str, FlagRule],
    user_id: str | None,
    user_segments: frozenset[str] = frozenset(),
) -> tuple[object, str]:
    """Evaluate a flag and return (value, reason)."""
    flag = flags.get(flag_key)
    if flag is None:
        return False, "DEFAULT"
    if not flag.enabled:
        return False, "DISABLED"
    for prereq in flag.prerequisites:
        parent = flags.get(prereq)
        if parent is None or not evaluate(prereq, flags, user_id, user_segments)[0]:
            return False, "PREREQUISITE_UNMET"
    if user_id is None:
        return False, "DEFAULT"  # anonymous traffic gets the default
    if user_id in flag.users_off:
        return False, "TARGETING_MATCH"
    if user_id in flag.users_on:
        return _variant_or_true(flag, user_id), "TARGETING_MATCH"
    if flag.segments_on & user_segments:
        return _variant_or_true(flag, user_id), "TARGETING_MATCH"
    if flag.percentage is not None:
        if bucket(flag.key, user_id) < flag.percentage:
            return _variant_or_true(flag, user_id), "SPLIT"
        return False, "DEFAULT"
    if flag.users_on or flag.users_off or flag.segments_on:
        return False, "DEFAULT"  # targeted flag; this user matched no rule
    return True, "SPLIT"  # pure toggle with no targeting rules


def _variant_or_true(flag: FlagRule, user_id: str) -> object:
    """Assign a stable A/B variant, or True for boolean flags."""
    if not flag.variants:
        return True
    return flag.variants[bucket(flag.key, user_id) % len(flag.variants)]
