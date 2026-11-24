#!/usr/bin/env bash
# Rollback drill: times each step of the documented rollback runbook.
# Usage:
#   ./rollback_drill.sh --rehearse staging   # timed rehearsal
#   ./rollback_drill.sh --check-recency --max-days 90   # CI gate check
set -euo pipefail

DRILL_LOG="${DRILL_LOG:-rollback_drill.log}"

timed_step() {
  local name="$1"; shift
  local start=$SECONDS
  "$@"
  local elapsed=$((SECONDS - start))
  echo "$(date -Iseconds) ${name}: ${elapsed}s" | tee -a "$DRILL_LOG"
}

if [[ "${1:-}" == "--check-recency" ]]; then
  max_days="${4:-90}"
  last=$(grep -c . "$DRILL_LOG" 2>/dev/null || echo 0)
  [[ "$last" -gt 0 ]] || { echo "No rollback drill recorded — NO-GO"; exit 1; }
  last_date=$(tail -1 "$DRILL_LOG" | cut -d' ' -f1 | cut -dT -f1)
  age=$(( ($(date +%s) - $(date -d "$last_date" +%s)) / 86400 ))
  [[ "$age" -le "$max_days" ]] || { echo "Drill is ${age}d old (> ${max_days}d) — NO-GO"; exit 1; }
  echo "Last drill ${age}d ago — OK"
  exit 0
fi

echo "== Rollback drill ($1) =="
timed_step "identify-previous-artifact" ./scripts/get_previous_release.sh
timed_step "revert-application" ./scripts/deploy.sh --version previous --env "$2"
timed_step "revert-schema-contract" ./scripts/migrate.sh --contract-only --env "$2"
timed_step "smoke-verify" ./scripts/smoke.sh --env "$2"
timed_step "verify-alerts-quiet" ./scripts/check_alerts.sh --env "$2"

total=$(awk -F': ' '{s+=$2} END {print s}' <(grep "$(date +%F)" "$DRILL_LOG"))
echo "Total rollback time: ${total}s — compare with documented runbook."
