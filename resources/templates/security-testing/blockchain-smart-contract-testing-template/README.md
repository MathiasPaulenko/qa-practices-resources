# Blockchain Smart Contract Testing Template — Companion

Downloadable files for the [Blockchain Smart Contract Testing Template](https://qapractices.com/templates/blockchain-smart-contract-testing-template/) on QAPractices.

## Contents

| File | Purpose |
|---|---|
| `smart-contract-testing-log.md` | Blank testing log with all eleven sections: contract details, test environment, unit coverage, access control, gas budget, vulnerability checklist, upgrade tests, integration, deployment verification, defect tracking and sign-off. |
| `smart-contract-testing-log-sample.md` | The same document filled end-to-end for a fictional pausable ERC-20 called SAFE on Polygon, tested with Foundry before an external audit. |

## Usage

1. Copy `smart-contract-testing-log.md` into your project docs, wiki or repo.
2. Fill Contract Details first — chain, Solidity version and framework decide which tools apply later.
3. Take test counts from `forge test` or `npx hardhat test` output, never from memory.
4. Log every failure in Defect Tracking with a severity before fixing it; auditors trace each SC-xxx back to the commit that resolved it.
5. Collect sign-offs only after deployment verification passes on the real network.

Use `smart-contract-testing-log-sample.md` as the reference for level of detail and realistic values.
