"""Pytest suite mirroring the resource's geofencing test cases."""

import math

import pytest

from geofence import (
    CircleGeofence,
    CooldownFilter,
    Debouncer,
    DwellTimer,
    haversine,
    point_in_polygon,
    simulate_drift,
)

STORE = CircleGeofence(lat=40.7589, lng=-73.9851, radius_m=100)


# --- haversine / coordinates (TC-018, TC-021, TC-022) ---

def test_haversine_known_distance():
    d = haversine(40.7128, -74.0060, 40.7130, -74.0060)
    assert 15 < d < 30  # ~22m northward


def test_haversine_antimeridian_wrap():
    # TC-018: lng 179.999 -> -179.999 is ~222m, not ~36,000km
    d = haversine(0, 179.999, 0, -179.999)
    assert d < 500


def test_haversine_pole():
    # TC-021: near the North Pole every longitude is a few hundred meters apart
    d = haversine(89.999, 0, 89.999, 180)
    assert d < 300


def test_haversine_large_geofence():
    # TC-022: 50km inside a 100km geofence
    big = CircleGeofence(lat=0, lng=0, radius_m=100_000)
    assert big.contains(0.2, 0.3)


# --- circle containment (TC-002, TC-016) ---

def test_entry_inside_radius():
    assert STORE.contains(40.7590, -73.9851)


def test_outside_radius():
    assert not STORE.contains(40.7610, -73.9851)


def test_boundary_inclusive():
    edge_lat = 40.7589 + (100 / 111_320)
    assert STORE.contains(edge_lat, -73.9851)


def test_tiny_radius_is_fragile():
    # TC-016: a 10m fence flaps under normal GPS error
    tiny = CircleGeofence(lat=40.7589, lng=-73.9851, radius_m=10)
    jittered = [40.75895, 40.75905]
    assert not all(tiny.contains(lat, -73.9851) for lat in jittered)


# --- drift / debounce (TC-013, TC-017) ---

def test_drift_no_false_entry():
    # TC-013: device ~111m outside the 100m fence, fixes wander but stay out
    fixes = [(40.7599 + i * 0.00002, -73.9851) for i in range(60)]
    assert simulate_drift(STORE, fixes, required=2) == []


def test_single_noisy_fix_suppressed():
    # one stray inside-fix must not trigger entry when required=2
    fixes = [(40.7599, -73.9851)] * 3 + [(40.7590, -73.9851)] + [(40.7599, -73.9851)] * 3
    assert simulate_drift(STORE, fixes, required=2) == []


def test_two_consecutive_fixes_trigger_entry():
    fixes = [(40.7590, -73.9851)] * 2
    assert simulate_drift(STORE, fixes, required=2) == ["entry"]


def test_exit_after_entry():
    fixes = [(40.7590, -73.9851)] * 2 + [(40.7610, -73.9851)]
    assert simulate_drift(STORE, fixes, required=2) == ["entry", "exit"]


# --- dwell (TC-004) ---

def test_dwell_fires_after_interval():
    t = DwellTimer(dwell_seconds=300)
    t.enter(0)
    assert not t.check(299, still_inside=True)
    assert t.check(300, still_inside=True)


def test_dwell_reset_on_early_exit():
    t = DwellTimer(dwell_seconds=300)
    t.enter(0)
    assert not t.check(200, still_inside=False)
    t.enter(400)
    assert t.check(700, still_inside=True)


def test_dwell_fires_once_per_stay():
    t = DwellTimer(dwell_seconds=300)
    t.enter(0)
    assert t.check(300, still_inside=True)
    assert not t.check(600, still_inside=True)


# --- polygon (TC-024) ---

SQUARE = [(0, 0), (0, 1), (1, 1), (1, 0)]


def test_point_inside_polygon():
    assert point_in_polygon(0.5, 0.5, SQUARE)


def test_point_outside_polygon():
    assert not point_in_polygon(1.5, 0.5, SQUARE)


def test_polygon_exit_through_different_edge():
    assert not point_in_polygon(0.5, -0.5, SQUARE)


# --- cooldown (TC-029) ---

def test_cooldown_suppresses_reentry():
    c = CooldownFilter(minutes=30)
    assert c.allow("GF-001", 0)
    assert not c.allow("GF-001", 1000)


def test_cooldown_expires():
    c = CooldownFilter(minutes=30)
    assert c.allow("GF-001", 0)
    assert c.allow("GF-001", 1800)


def test_cooldown_is_per_geofence():
    c = CooldownFilter(minutes=30)
    assert c.allow("GF-001", 0)
    assert c.allow("GF-002", 0)
