#!/usr/bin/env bash
# hotfix-scope-check.sh — verify a hotfix branch contains only the fix.
#
# A hotfix ships on a ticking clock: every commit beyond the fix is unreviewed
# risk. This script lists what the hotfix branch adds on top of the production
# tag and fails if there is more than one commit.
#
# Usage:
#   ./hotfix-scope-check.sh v1.2.3 hotfix/1.2.4
#
# Exit codes:
#   0 — scope is clean (exactly one commit on top of the tag)
#   1 — usage error or missing refs
#   2 — scope violation (more than one commit, or branch not based on the tag)

set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <production-tag> <hotfix-branch>" >&2
  echo "Example: $0 v1.2.3 hotfix/1.2.4" >&2
  exit 1
fi

TAG="$1"
BRANCH="$2"

git rev-parse --verify --quiet "$TAG" >/dev/null || {
  echo "ERROR: tag '$TAG' does not exist. Branch from the production tag, not develop." >&2
  exit 1
}
git rev-parse --verify --quiet "$BRANCH" >/dev/null || {
  echo "ERROR: branch '$BRANCH' does not exist." >&2
  exit 1
}

# The hotfix branch must contain the production tag as an ancestor — otherwise
# it was branched from the wrong base and carries extra history.
if ! git merge-base --is-ancestor "$TAG" "$BRANCH"; then
  echo "FAIL: '$BRANCH' is not based on production tag '$TAG'." >&2
  echo "Branch from the tag: git checkout -b $BRANCH $TAG" >&2
  exit 2
fi

COMMITS=$(git log --oneline "$TAG..$BRANCH")
COUNT=$(echo "$COMMITS" | wc -l | tr -d ' ')

echo "Commits on $BRANCH since $TAG:"
echo "$COMMITS"
echo

if [ "$COUNT" -ne 1 ]; then
  echo "FAIL: expected exactly 1 commit (the fix), found $COUNT." >&2
  echo "Every extra commit is unreviewed risk — split it out before deploying." >&2
  exit 2
fi

echo "PASS: clean scope — one fix commit on top of $TAG."
