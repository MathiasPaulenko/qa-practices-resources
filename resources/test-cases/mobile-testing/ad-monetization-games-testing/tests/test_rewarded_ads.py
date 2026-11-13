from ad_service import FakeRewardedAdSDK, RewardLedger


def test_reward_granted_once_on_completion():
    sdk = FakeRewardedAdSDK(duration_seconds=30)
    ledger = RewardLedger(balance=1_000)
    sdk.play(watched_seconds=30)
    ledger.apply(sdk)
    assert ledger.balance == 1_500
    assert sdk.pending_reward == 0  # replaying must not double-grant


def test_no_reward_on_early_close():
    sdk = FakeRewardedAdSDK(duration_seconds=30)
    ledger = RewardLedger(balance=1_000)
    sdk.play(watched_seconds=12)
    ledger.apply(sdk)
    assert ledger.balance == 1_000


def test_second_play_needs_a_fresh_ad():
    sdk = FakeRewardedAdSDK(duration_seconds=30)
    ledger = RewardLedger(balance=1_000)
    sdk.play(watched_seconds=30)
    ledger.apply(sdk)
    sdk.play(watched_seconds=30)  # cached ad already consumed
    ledger.apply(sdk)
    assert ledger.balance == 1_500
