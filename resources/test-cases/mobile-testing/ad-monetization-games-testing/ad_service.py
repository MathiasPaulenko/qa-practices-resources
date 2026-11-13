"""Offline fakes for testing ad monetization logic without a device or SDK."""

from datetime import datetime, timezone


class FakeRewardedAdSDK:
    """Mimics a rewarded-ad SDK: the reward callback only fires on full completion."""

    def __init__(self, duration_seconds: int = 30) -> None:
        self.duration_seconds = duration_seconds
        self.loaded = True
        self.pending_reward = 0

    def play(self, watched_seconds: int) -> str:
        """Plays the cached ad once; returns the callback the real SDK would fire."""
        if not self.loaded:
            return "on_ad_failed_to_show"
        self.loaded = False
        if watched_seconds >= self.duration_seconds:
            self.pending_reward = 500
            return "on_user_earned_reward"
        return "on_ad_closed_early"


class RewardLedger:
    """In-memory coin balance; apply() drains the SDK's pending reward exactly once."""

    def __init__(self, balance: int = 0) -> None:
        self.balance = balance

    def apply(self, sdk: FakeRewardedAdSDK) -> int:
        granted = sdk.pending_reward
        sdk.pending_reward = 0
        self.balance += granted
        return granted


class FrequencyCapper:
    """Per-placement frequency cap backed by the system clock (mockable)."""

    def __init__(self, interval_seconds: int = 300) -> None:
        self.interval_seconds = interval_seconds
        self._last_shown: datetime | None = None

    def record_impression(self) -> None:
        self._last_shown = datetime.now(timezone.utc)

    def can_show(self) -> bool:
        if self._last_shown is None:
            return True
        elapsed = (datetime.now(timezone.utc) - self._last_shown).total_seconds()
        return elapsed >= self.interval_seconds
