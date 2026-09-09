#!/usr/bin/env bash
# Launchable predictive test selection.
#
# Requires: Launchable CLI installed and LAUNCHABLE_API_KEY set.
# Usage: bash launchable_subset.sh <build_name> <target_percentage>

set -euo pipefail

BUILD_NAME="${1:-$(date +%Y%m%d-%H%M%S)}"
TARGET="${2:-30%}"

echo "=== Launchable Predictive Test Selection ==="
echo "Build: $BUILD_NAME"
echo "Target subset: $TARGET"
echo ""

# Record test results after a full run to train the model
echo "[1/3] Recording test results..."
launchable record tests --build "$BUILD_NAME" pytest reports/

# Request a subset of the most relevant tests for this change
echo "[2/3] Requesting $TARGET subset..."
launchable subset --target "$TARGET" --build "$BUILD_NAME" pytest > subset.txt

# Run only the selected subset
echo "[3/3] Running selected subset..."
echo "Selected tests: $(wc -l < subset.txt)"
pytest "$(cat subset.txt)"

echo "Done. Subset ran successfully."
