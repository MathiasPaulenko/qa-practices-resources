# Blockchain Smart Contract Testing — Foundry Example

A minimal, runnable Foundry project used in the QAPractices guide:

- [Blockchain & Smart Contract Testing Guide](https://qapractices.com/documentation/blockchain-smart-contract-testing-guide/)

It covers the test patterns the guide recommends: unit tests, fuzz tests, revert
conditions, event assertions, and a reentrancy-attacker contract that proves the
vault's checks-effects-interactions ordering actually protects funds.

## Setup

```bash
# Install Foundry (forge, cast, anvil)
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Install dependencies (forge-std)
forge install foundry-rs/forge-std --no-commit
```

## Run

```bash
forge test                      # full suite
forge test -vvv                 # verbose traces
forge test --gas-report         # per-function gas table
forge snapshot                  # write .gas-snapshot for CI diffs
forge test --fork-url $MAINNET_RPC_URL   # run against a mainnet fork
```

## Project structure

```text
├── foundry.toml                  # solc 0.8.24, fuzz runs for CI profile
├── src/
│   └── SimpleVault.sol           # deposit/withdraw vault (checks-effects-interactions)
├── test/
│   ├── SimpleVault.t.sol         # unit, fuzz, revert and event tests
│   └── ReentrancyExploit.t.sol   # malicious receiver that fails to re-enter
└── .github/workflows/foundry.yml # CI: build + test + gas snapshot
```

## What the tests demonstrate

| Test file | Pattern |
|---|---|
| `testDepositUpdatesBalance` | happy path + `vm.prank` + `vm.deal` |
| `testWithdrawInsufficientBalanceReverts` | `vm.expectRevert` on a revert condition |
| `testDepositEmitsEvent` | `vm.expectEmit` event assertion |
| `testFuzz_DepositWithinBalance` | input fuzzing with `vm.assume` |
| `testFuzz_WithdrawNeverExceedsDeposit` | property-style fuzz on a revert path |
| `testReentrantWithdrawFails` | attacker contract re-entering `withdraw` — fails because state is zeroed first |

Expected output (truncated):

```text
[PASS] testDepositEmitsEvent() (gas: 42581)
[PASS] testDepositUpdatesBalance() (gas: 58732)
[PASS] testFuzz_DepositWithinBalance(uint96) (runs: 256)
[PASS] testReentrantWithdrawFails() (gas: 210445)
[PASS] testWithdrawInsufficientBalanceReverts() (gas: 13872)
```
