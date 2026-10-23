# Geofencing Location Alert Test Cases — Runnable Companion

Companion code for [Geofencing Location Alert Test Cases](https://qapractices.com/test-cases/geofencing-location-alert-test-cases/) on QAPractices.

## What is here

`geofence.py` — stdlib-only primitives that mirror the logic a real geofencing feature needs:

- `haversine()` — great-circle distance with antimeridian (±180°) wrap.
- `CircleGeofence` — containment check by radius.
- `point_in_polygon()` — ray-casting, for app-level polygon fences (native OS geofencing is circle-only).
- `Debouncer` — N-consecutive-fix smoothing against GPS drift false entries.
- `DwellTimer` — entry + interval, resets on early exit.
- `CooldownFilter` — per-geofence alert suppression.
- `simulate_drift()` — feeds a fix sequence through the debouncer.

`tests/test_geofence.py` — 21 pytest cases mapped to the resource:

| Resource case | Covered by |
|---|---|
| TC-002 Entry | `test_entry_inside_radius`, `test_boundary_inclusive` |
| TC-004 Dwell | `test_dwell_*` |
| TC-013 GPS drift | `test_drift_*`, `test_single_noisy_fix_suppressed` |
| TC-016 Min radius | `test_tiny_radius_is_fragile` |
| TC-018 Antimeridian | `test_haversine_antimeridian_wrap` |
| TC-021 Poles | `test_haversine_pole` |
| TC-022 100km fence | `test_haversine_large_geofence` |
| TC-024 Polygon | `test_point_*polygon*` |
| TC-029 Cooldown | `test_cooldown_*` |

## Run

```bash
pip install -r requirements.txt
pytest tests/ -q
```

Python 3.10+, no third-party dependencies beyond pytest.
