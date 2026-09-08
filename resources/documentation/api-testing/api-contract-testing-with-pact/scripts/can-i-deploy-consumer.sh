#!/usr/bin/env bash
# can-i-deploy-consumer.sh
# Can-I-Deploy check for a consumer
set -euo pipefail

pact-broker can-i-deploy \
  --pacticipant "billing-service" \
  --version "1.2.3" \
  --to-environment "production" \
  --broker-base-url "${PACT_BROKER_URL:-https://pact-broker.qa.local}" \
  --broker-token "${PACT_TOKEN}"
