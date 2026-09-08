# API Contract Testing with Pact — Companion Scripts

> Companion resource for [API Contract Testing with Pact: Consumer-Driven Contracts](https://qapractices.com/documentation/api-contract-testing-with-pact) on QAPractices.com.

Scripts for consumer-driven contract testing with Pact JS 13.x and Pact Python 2.x. Includes consumer tests, provider verification, publish scripts, can-i-deploy checks, and a CI/CD workflow.

## Requirements

- Node.js 20+
- npm 10+
- `@pact-foundation/pact` 13.x
- Python 3.12+ (for Python examples)
- `pact-python` 2.x (for Python examples)
- A running Pact Broker (e.g. `https://pact-broker.qa.local`)

## Setup

```bash
# Clone and install
npm init -y
npm install @pact-foundation/pact@13 @pact-foundation/pact-node@14

# For Python examples
pip install pact-python==2.* requests==2.32

# Run consumer tests
npm run test:consumer

# Run provider verification
npm run test:provider

# Publish pacts to broker
node scripts/publish-pacts.js

# Can-I-Deploy check
pact-broker can-i-deploy \
  --pacticipant UserService \
  --version 2.4.1 \
  --to-environment production \
  --broker-base-url https://pact-broker.qa.local \
  --broker-token $PACT_TOKEN
```

## Files

| File | Purpose |
| ------ | --------- |
| `scripts/consumer.test.js` | Consumer contract test using PactV3 |
| `scripts/provider.test.js` | Provider verification against real API |
| `scripts/publish-pacts.js` | Publish Pact files to the broker |
| `scripts/python_consumer_test.py` | Python consumer test with pact-python 2.x |
| `scripts/can-i-deploy-consumer.sh` | Can-I-Deploy check for a consumer |
| `scripts/cli-provider-verify.sh` | CLI provider verification with pact-verifier |
| `.github/workflows/contract-tests.yml` | CI/CD workflow for consumer + provider jobs |

## Architecture

The scripts follow the contract testing flow:

1. Consumer test generates a Pact file (JSON artifact).
2. Pact file is published to the Pact Broker.
3. Provider fetches contracts from the broker and verifies against the real API.
4. Verification results are published back to the broker.
5. `can-i-deploy` queries the broker before any deployment.

## License

MIT — free to use, modify, and distribute.
