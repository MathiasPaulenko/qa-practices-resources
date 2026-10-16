"""Tests for the anti-cheat reference checks (TC-01, TC-02, TC-07 of the article)."""

from anticheat_checks import (
    aim_snap_rate,
    bans_missing_evidence,
    validate_move,
)


def test_speed_hack_is_flagged() -> None:
    # TC-01: 1000 units in 1s against a 500 u/s limit
    assert validate_move((0, 0), (1000, 0), 1.0).startswith("flag")


def test_legal_speed_within_jitter_margin_passes() -> None:
    # TC-01 / edge: 520 u/s is above nominal max but inside the 15% jitter margin
    assert validate_move((0, 0), (520, 0), 1.0) == "ok"


def test_zero_dt_never_crashes_and_flags() -> None:
    # A zero-delta report means infinite speed — flag, don't divide by zero
    assert validate_move((0, 0), (1, 0), 0.0).startswith("flag")


def test_aimbot_snap_rate_detected() -> None:
    # TC-02: bot snapping in <50ms on every engagement vs a human spread
    bot = aim_snap_rate([40, 45, 50, 38, 49] * 6)
    human = aim_snap_rate([180, 220, 150, 400, 130] * 6)
    assert bot > 0.9
    assert human < 0.2


def test_ban_without_evidence_is_audited() -> None:
    # TC-07: a ban missing confidence_score or replay_url must surface in audit
    log = [
        {"player_id": 1, "action": "ban", "confidence_score": 0.97, "replay_url": "r/1"},
        {"player_id": 2, "action": "ban", "confidence_score": None, "replay_url": None},
        {"player_id": 3, "action": "flag", "confidence_score": 0.5, "replay_url": None},
    ]
    missing = bans_missing_evidence(log)
    assert [b["player_id"] for b in missing] == [2]
