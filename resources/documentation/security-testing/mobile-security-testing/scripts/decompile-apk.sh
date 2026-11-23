#!/usr/bin/env bash
# Decompiles an APK with apktool 2.9+ and points at the files worth reviewing.
set -euo pipefail

APK="${1:?Usage: $0 <app.apk>}"
OUT="${APK%.apk}-decompiled"

apktool d "$APK" -o "$OUT"

echo "== Files to review =="
echo "  $OUT/AndroidManifest.xml            (debuggable, cleartext, exported components, permissions)"
echo "  $OUT/res/xml/network_security_config.xml  (pinning, user CA trust)"
find "$OUT/res" -name "*.xml" -path "*network*" -print 2>/dev/null || true
