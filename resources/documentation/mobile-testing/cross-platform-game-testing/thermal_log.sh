#!/usr/bin/env bash
# Samples the hottest Android thermal zone while a game session runs.
# Requires a connected device with USB debugging (adb).
#
# Usage: ./thermal_log.sh 1800 thermal_log.csv
#   $1 — duration in seconds (default 1800 = 30 min sustained session)
#   $2 — output CSV (default thermal_log.csv)
#
# Pair with: adb shell dumpsys gfxinfo <package> framestats
# to correlate frame times with the temperature curve.

DURATION=${1:-1800}
OUT=${2:-thermal_log.csv}

echo "timestamp_ms,max_temp_c" > "$OUT"
end=$(( $(date +%s) + DURATION ))

while [ "$(date +%s)" -lt "$end" ]; do
  ts=$(date +%s%3N)
  max=$(adb shell 'for z in /sys/class/thermal/thermal_zone*/temp; do cat "$z"; done' 2>/dev/null \
    | tr -d '\r' \
    | awk '{if ($1 > m) m = $1} END {printf "%.1f", m / 1000}')
  echo "$ts,$max" >> "$OUT"
  sleep 5
done
