#!/usr/bin/env bash
# Audits the internal storage of a debuggable app via adb run-as.
# Flags files that commonly hold tokens or PII in plain text.
set -euo pipefail

PKG="${1:?Usage: $0 <package.name>  e.g. com.acme.banking}"

echo "== Directory tree for $PKG =="
adb shell run-as "$PKG" ls -R shared_prefs files databases 2>/dev/null || {
  echo "run-as failed: is the build debuggable and installed?" >&2
  exit 1
}

echo
echo "== shared_prefs contents (look for tokens, PII, feature flags) =="
for f in $(adb shell run-as "$PKG" ls shared_prefs 2>/dev/null | tr -d '\r'); do
  echo "--- shared_prefs/$f"
  adb shell run-as "$PKG" cat "shared_prefs/$f" 2>/dev/null | head -40
done
