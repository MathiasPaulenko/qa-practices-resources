#!/usr/bin/env bash
# Send a mock GPS location to an Android emulator or real device.
# Usage: ./mock_location.sh <emulator|device> <lat> <lng>
set -euo pipefail

TARGET="${1:?usage: mock_location.sh <emulator|device> <lat> <lng>}"
LAT="${2:?latitude required}"
LNG="${3:?longitude required}"

case "$TARGET" in
  emulator)
    # First emulator listens on telnet console port 5554
    (echo "geo fix $LNG $LAT"; sleep 1) | telnet localhost 5554
    echo "Mock fix sent to emulator: $LAT, $LNG"
    ;;
  device)
    PKG="${PKG:-com.example.app}"
    adb shell appops set "$PKG" android:mock_location allow
    adb shell am broadcast -a "$PKG.mocklocation" --ef lat "$LAT" --ef lng "$LNG"
    echo "Mock location enabled and fix sent on device ($PKG): $LAT, $LNG"
    ;;
  *)
    echo "unknown target: $TARGET (use emulator|device)" >&2
    exit 1
    ;;
esac
