#!/usr/bin/env bash
# Diff component lists between two CycloneDX SBOMs to detect drift.
# Usage: ./drift-check.sh old.cdx.json new.cdx.json
set -euo pipefail
OLD="${1:?old sbom required}"
NEW="${2:?new sbom required}"
python3 - "$OLD" "$NEW" <<'PY'
import json, sys
def names(p):
    return {c["name"] + "@" + c.get("version", "?") for c in json.load(open(p))["components"]}
old, new = names(sys.argv[1]), names(sys.argv[2])
print("Added:", *sorted(new - old), sep="\n  ")
print("Removed:", *sorted(old - new), sep="\n  ")
PY
