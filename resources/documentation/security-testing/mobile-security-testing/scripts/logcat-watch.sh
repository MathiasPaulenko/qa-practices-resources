#!/usr/bin/env bash
# Watches logcat for lines that look like credential or token leaks.
# Exercise the login, payment and logout flows while this runs.
set -euo pipefail

PKG="${1:-}"
FILTER='token|password|passwd|secret|bearer|authorization|session|credential'

if [ -n "$PKG" ]; then
  PID=$(adb shell pidof "$PKG" | tr -d '\r')
  adb logcat --pid="$PID" | grep -iE "$FILTER"
else
  adb logcat | grep -iE "$FILTER"
fi
