# Smart Contract Testing Log — Completed Sample

> Filled example for a fictional pausable ERC-20 called **SAFE** on Polygon, tested with Foundry before an external audit.
> Companion to https://qapractices.com/templates/blockchain-smart-contract-testing-template/

## Contract Details

| Field | Details |
|---|---|
| **Contract name** | SAFEToken (ERC-20, pausable) |
| **Network** | Polygon |
| **Solidity version** | 0.8.24 |
| **Framework** | Foundry, release 2024-10 |
| **Test lead** | David Okafor |
| **Test dates** | 2025-01-06 to 2025-01-15 |
| **Audit target** | Yes, Trail of Bits |

---

## Test Environment

| Environment | Purpose | Chain | Notes |
|---|---|---|---|
| **Local (Anvil)** | Unit and integration tests | Local | 51 tests, ~400ms |
| **Testnet (Sepolia)** | Staging validation | Sepolia | Deploy script + explorer verification |
| **Fork mainnet** | Real state testing | Polygon fork @ block 51800000 | USDC pair liquidity checks |
| **Mainnet** | Production deployment | Polygon | Pending sign-off |

---

## Unit Test Coverage

### Function-Level Coverage

| Function | Visibility | Tests Written | Coverage | Status | Notes |
|---|---|---|---|---|---|
| `transfer()` | external | 8 | 100% | [x] | Includes zero-address revert |
| `approve()` | external | 5 | 100% | [x] | Allowance race covered |
| `transferFrom()` | external | 7 | 100% | [x] | Insufficient allowance path |
| `mint()` | external | 6 | 100% | [x] | Only owner; cap enforced |
| `burn()` | external | 5 | 100% | [x] | Only owner |
| `pause()` | external | 3 | 100% | [x] | Emits Paused event |
| `withdraw()` | external | 6 | 100% | [x] | Reentrancy guard verified |

### Test Categories

| Category | Test Count | Status | Notes |
|---|---|---|---|
| **Happy path** | 15 | [x] | |
| **Revert conditions** | 22 | [x] | All revert strings asserted |
| **Access control** | 12 | [x] | |
| **Edge cases** | 18 | [x] | Zero and max uint256 covered |
| **Event emission** | 10 | [x] | |

---

## Access Control Tests

| Test ID | Scenario | Caller | Expected | Status | Notes |
|---|---|---|---|---|---|
| AC-001 | Owner calls mint | 0xDepl0yer | Success | [x] | Minted 1000 SAFE |
| AC-002 | Non-owner calls mint | 0xR4ndom | Revert `OwnableUnauthorizedAccount` | [x] | |
| AC-005 | Renounce ownership | Owner | Success, no owner | [x] | Delayed until post-deploy |
| AC-006 | Paused contract transfer | User | Revert `EnforcedPause` | [x] | |

---

## Security Tests (excerpt)

| Vulnerability | Test Method | Status | Notes |
|---|---|---|---|
| **Reentrancy** | NonReentrant pattern + test | [x] | Found via Slither, fixed in `a1f9c2` |
| **Access control bypass** | Role-based tests for all functions | [x] | |
| **Signature replay** | Nonce + chainId in signature | [ ] | N/A — no permit() yet |

---

## Deployment Verification

| Test ID | Check | Expected | Status | Notes |
|---|---|---|---|---|
| DEP-001 | Contract deployed at correct address | Address matches | [x] | Sepolia dry run |
| DEP-003 | Initial state correct | Supply, roles, params | [x] | 10M SAFE, cap 100M |
| DEP-006 | Verified on block explorer | Source code verified | [ ] | Pending mainnet |

---

## Defect Tracking

| Defect ID | Category | Severity | Description | Status | Notes |
|---|---|---|---|---|---|
| SC-001 | Security | Critical | Reentrancy in `withdraw` before checks-effects-interactions | [x] | Fixed in commit `a1f9c2` |
| SC-003 | Logic | High | `mint` allowed minting to the zero address | [x] | Fixed in commit `b3d4e8` |

---

## Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| **QA Lead** | David Okafor | 2025-01-15 | Conditional — pending DEP-006 |
| **Smart Contract Dev** | Isabelle Dubois | 2025-01-15 | Approved |
| **Security Auditor** | Aisha Hassan | 2025-01-16 | Approved |
| **Product Owner** | Liam O'Brien | 2025-01-16 | Approved |
