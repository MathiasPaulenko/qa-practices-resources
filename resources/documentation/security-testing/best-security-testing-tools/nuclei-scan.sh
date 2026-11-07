#!/usr/bin/env bash
# Nuclei targeted scan — template-driven checks for specific CVEs/exposures.
# Usage: ./nuclei-scan.sh https://staging.example.com
# Requires: nuclei v3 (https://github.com/projectdiscovery/nuclei)

set -euo pipefail

TARGET_URL="${1:?Usage: $0 <target-url>}"

nuclei -u "$TARGET_URL" \
  -severity critical,high \
  -rl 10
