#!/usr/bin/env bash
# Manage Android runtime permissions for manual and automated testing.
# Usage: ./permission_adb.sh <package> <action> [permission]
# Actions: grant | revoke | reset | dump
# Example: ./permission_adb.sh com.example.app grant android.permission.CAMERA

set -euo pipefail

PKG="${1:?Usage: $0 <package> <grant|revoke|reset|dump> [permission]}"
ACTION="${2:?Usage: $0 <package> <grant|revoke|reset|dump> [permission]}"
PERM="${3:-}"

case "$ACTION" in
  grant)
    [ -n "$PERM" ] || { echo "grant requires a permission name"; exit 1; }
    adb shell pm grant "$PKG" "$PERM"
    ;;
  revoke)
    [ -n "$PERM" ] || { echo "revoke requires a permission name"; exit 1; }
    adb shell pm revoke "$PKG" "$PERM"
    ;;
  reset)
    # Restores all runtime permissions to install state
    adb shell pm reset-permissions "$PKG"
    ;;
  dump)
    # Shows every declared permission and its grant state
    adb shell dumpsys package "$PKG" | grep -E "permission|granted" | head -60
    ;;
  *)
    echo "Unknown action: $ACTION (expected grant|revoke|reset|dump)"; exit 1;;
esac
