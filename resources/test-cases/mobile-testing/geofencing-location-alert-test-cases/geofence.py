"""Geofence primitives for the geofencing-location-alert-test-cases companion.

Stdlib-only: haversine distance with antimeridian wrap, circle and polygon
containment, drift debounce, dwell scheduling and cooldown filtering.
"""

import math
from dataclasses import dataclass, field

EARTH_RADIUS_M = 6_371_000


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in meters; wraps longitude across +-180."""
    d_lon = ((lon2 - lon1 + 540) % 360) - 180
    phi = math.radians(lat2 - lat1)
    lam = math.radians(d_lon)
    a = math.sin(phi / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(lam / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.atan2(math.sqrt(a), math.sqrt(1 - a))


@dataclass
class CircleGeofence:
    lat: float
    lng: float
    radius_m: float

    def contains(self, lat: float, lng: float) -> bool:
        return haversine(self.lat, self.lng, lat, lng) <= self.radius_m


def point_in_polygon(lat: float, lng: float, vertices: list[tuple[float, float]]) -> bool:
    """Ray-casting containment; vertices are (lat, lng) pairs."""
    inside = False
    n = len(vertices)
    j = n - 1
    for i in range(n):
        yi, xi = vertices[i]
        yj, xj = vertices[j]
        if (xi > lng) != (xj > lng) and lat < (yj - yi) * (lng - xi) / (xj - xi) + yi:
            inside = not inside
        j = i
    return inside


class Debouncer:
    """Fires a transition only after `required` consecutive in-zone fixes.

    Mirrors the smoothing real geofencing code needs so a single noisy fix
    under high reported accuracy does not produce a false entry.
    """

    def __init__(self, required: int = 2):
        self.required = required
        self._streak = 0
        self.inside = False

    def feed(self, inside_zone: bool) -> str | None:
        """Returns 'entry', 'exit' or None for each location fix."""
        if inside_zone:
            self._streak += 1
            if not self.inside and self._streak >= self.required:
                self.inside = True
                self._streak = 0
                return "entry"
        else:
            self._streak = 0
            if self.inside:
                self.inside = False
                return "exit"
        return None


class DwellTimer:
    """Entry + dwell_seconds produces a dwell event only on continuous stay."""

    def __init__(self, dwell_seconds: float):
        self.dwell = dwell_seconds
        self._entered_at: float | None = None

    def enter(self, t: float) -> None:
        self._entered_at = t

    def check(self, t: float, still_inside: bool) -> bool:
        if self._entered_at is None:
            return False
        if not still_inside:
            self._entered_at = None
            return False
        if t - self._entered_at >= self.dwell:
            self._entered_at = None  # dwell fires once per stay
            return True
        return False


@dataclass
class CooldownFilter:
    """Per-geofence alert suppression; transitions still get logged."""

    minutes: float
    _last_alert: dict = field(default_factory=dict)

    def allow(self, geofence_id: str, t_seconds: float) -> bool:
        last = self._last_alert.get(geofence_id)
        if last is not None and t_seconds - last < self.minutes * 60:
            return False
        self._last_alert[geofence_id] = t_seconds
        return True


def simulate_drift(
    geofence: CircleGeofence,
    fixes: list[tuple[float, float]],
    required: int = 2,
) -> list[str]:
    """Feed a sequence of (lat, lng) fixes through the debouncer."""
    d = Debouncer(required)
    return [e for e in (d.feed(geofence.contains(*f)) for f in fixes) if e]
