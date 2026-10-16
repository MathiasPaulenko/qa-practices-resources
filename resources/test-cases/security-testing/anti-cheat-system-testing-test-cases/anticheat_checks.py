"""Reference anti-cheat checks for the companion of
test-cases/anti-cheat-system-testing-test-cases.

Server-side validators a game backend can run on client reports:
velocity checks, aim-snap heuristics and ban-evidence auditing.
"""

from __future__ import annotations


def validate_move(
    prev_pos: tuple[float, float],
    new_pos: tuple[float, float],
    dt_seconds: float,
    max_speed: float = 500.0,
    jitter_margin: float = 1.15,
) -> str:
    """Flag position updates that exceed the physics model's top speed.

    ``jitter_margin`` absorbs measurement noise on jittery connections —
    the server timestamp is authoritative, never the client's own delta.
    """
    dx = new_pos[0] - prev_pos[0]
    dy = new_pos[1] - prev_pos[1]
    distance = (dx * dx + dy * dy) ** 0.5
    speed = distance / dt_seconds if dt_seconds > 0 else float("inf")
    if speed > max_speed * jitter_margin:
        return f"flag: {speed:.0f} u/s exceeds {max_speed * jitter_margin:.0f} u/s"
    return "ok"


def aim_snap_rate(snaps_ms: list[float], threshold_ms: float = 100.0) -> float:
    """Fraction of aim snaps faster than a humanly plausible threshold."""
    if not snaps_ms:
        return 0.0
    fast = sum(1 for s in snaps_ms if s <= threshold_ms)
    return fast / len(snaps_ms)


def ban_has_evidence(ban: dict) -> bool:
    """A ban is only enforceable with a confidence score and a replay link."""
    return bool(ban.get("confidence_score") and ban.get("replay_url"))


def bans_missing_evidence(ban_log: list[dict]) -> list[dict]:
    """Audit helper: bans stored without evidence (SQL equivalent in the article)."""
    return [
        b for b in ban_log
        if b.get("action") == "ban" and not ban_has_evidence(b)
    ]
