#!/usr/bin/env bash
# Starts MobSF 4.x for static analysis of APK / IPA files.
# After it boots, open http://localhost:8000 and upload the binary.
set -euo pipefail

docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest
