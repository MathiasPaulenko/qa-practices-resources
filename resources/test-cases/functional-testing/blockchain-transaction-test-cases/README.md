# Blockchain Transaction Test Cases — Companion

Executable companion for [Blockchain Transaction Test Cases](https://qapractices.com/test-cases/blockchain-transaction-test-cases).

## Contents

| File | Description |
|---|---|
| `hardhat-transaction.test.js` | Hardhat 2.22 + ethers 6.x test suite covering TC-01, TC-02, TC-06, TC-12 and TC-19 |
| `GuardedVault.sol` | Minimal `onlyOwner` contract used by the authorization test (TC-19) |

## Usage

```bash
npm install --save-dev hardhat @nomicfoundation/hardhat-ethers ethers chai
npx hardhat init # or drop these files into an existing hardhat project
cp GuardedVault.sol contracts/
npx hardhat test hardhat-transaction.test.js
```

For the edge cases that need chain control (nonce gaps, reorgs, manual mining), run against Anvil instead:

```bash
anvil --no-mining   # submit txs, then mine manually to observe pending state
```
