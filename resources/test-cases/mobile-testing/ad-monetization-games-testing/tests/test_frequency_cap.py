from freezegun import freeze_time

from ad_service import FrequencyCapper


def test_first_interstitial_allowed():
    capper = FrequencyCapper(interval_seconds=300)
    assert capper.can_show() is True


def test_second_interstitial_blocked_inside_window():
    capper = FrequencyCapper(interval_seconds=300)
    with freeze_time("2026-01-01 12:00:00"):
        capper.record_impression()
        assert capper.can_show() is False


def test_cap_resets_after_interval():
    capper = FrequencyCapper(interval_seconds=300)
    with freeze_time("2026-01-01 12:00:00"):
        capper.record_impression()
    with freeze_time("2026-01-01 12:05:01"):
        assert capper.can_show() is True
