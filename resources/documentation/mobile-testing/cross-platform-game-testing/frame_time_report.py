"""Frame-time report for cross-platform game performance captures.

Reads a CSV with a `frame_ms` column (milliseconds per frame) and prints
average fps, the 1% low fps, and the stutter count (frames above 33 ms,
i.e. below ~30 fps). Python 3.12+, stdlib only.

Usage:
    python frame_time_report.py frame_times_sample.csv
"""

import csv
import sys

STUTTER_MS = 33.0


def analyze(path: str) -> None:
    with open(path, newline="") as f:
        times = [float(r["frame_ms"]) for r in csv.DictReader(f)]
    if not times:
        sys.exit("no frames in capture")
    times.sort()
    avg_ms = sum(times) / len(times)
    p1_index = min(int(len(times) * 0.99), len(times) - 1)
    stutters = sum(1 for t in times if t > STUTTER_MS)
    print(
        f"frames: {len(times)} | avg fps: {1000 / avg_ms:.1f} | "
        f"1% low: {1000 / times[p1_index]:.1f} | stutters: {stutters}"
    )


if __name__ == "__main__":
    analyze(sys.argv[1])
