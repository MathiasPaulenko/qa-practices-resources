#!/usr/bin/env bash
# cli-provider-verify.sh
# CLI provider verification with pact-verifier
set -euo pipefail

pact-verifier \
  --provider "UserService" \
  --provider-app-version "2.3.1" \
  --pact-broker-base-url "${PACT_BROKER_URL:-https://pact-broker.qa.local}" \
  --pact-broker-token "${PACT_TOKEN}" \
  --provider-base-url "http://localhost:3000" \
  --publish-verification-results
