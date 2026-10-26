#!/usr/bin/env bash
# Schema diff check for CI. Fails the build on breaking changes.
# Requires: npx @graphql-inspector/cli (7.x)
# Usage: ./schema-diff.sh schema-old.graphql schema-new.graphql
set -euo pipefail

OLD_SCHEMA="${1:?path to the previous schema SDL}"
NEW_SCHEMA="${2:?path to the new schema SDL}"

npx @graphql-inspector/cli diff "$OLD_SCHEMA" "$NEW_SCHEMA" \
  --rule suppressRemovalOfDeprecatedField
