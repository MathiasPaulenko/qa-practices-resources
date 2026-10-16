# AI Prompt: Blockchain Smart Contract Test Cases — Companion

Companion files for the [AI Prompt: Generate Blockchain Smart Contract Test Cases](https://qapractices.com/prompts/ai-prompt-blockchain-smart-contract-test-cases/) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full prompt template, ready to copy-paste into any LLM. |
| `example-input.txt` | Filled example input: a TokenVault ERC4626-style contract on Solidity ^0.8.24 behind a UUPS proxy. |
| `TokenVault.t.sol` | A runnable Foundry test file — the kind of output the prompt should produce: deposit/withdraw correctness, boundary reverts, a reentrancy attempt (SWC-107) with a helper attacker contract, access control and pause checks. |

## Usage

1. Copy `prompt-template.txt` into your LLM (ChatGPT, Claude, Copilot-style assistants).
2. Replace the bracketed placeholders with your contract context — or run it verbatim against `example-input.txt`.
3. Compare the generated cases with `TokenVault.t.sol` to sanity-check format and depth: each case should map to a real test function.
4. To run the sample suite: `forge init --no-git vault-test`, drop `TokenVault.t.sol` into `test/`, `forge install OpenZeppelin/openzeppelin-contracts`, then `forge test`.

## Requirements

- Any LLM for the prompt itself.
- [Foundry](https://book.getfoundry.sh/) (`forge`) and OpenZeppelin Contracts 5.x to run `TokenVault.t.sol`.

## Follow-up prompts

After generating the test cases, continue the conversation with:

- "Convert these test cases into a complete Foundry test file — setup, fixtures and the attacker helper contract included."
- "Write an invariant suite for this contract: list the properties that must always hold (totalSupply equals the sum of balances, the vault can't pay out more than it holds) as forge invariant tests."
- "Generate a Foundry fuzz configuration for the deposit/withdraw round-trip: run count, input bounds and the properties to check."
- "Produce a Slither 0.10.x configuration plus a triage checklist separating findings that matter from noise."

## Notes

- Generated test cases are scaffolding, not audit coverage — review them before trusting the suite.
- Never paste private keys, seed phrases or funded mainnet addresses into the prompt.
- Gas numbers the model returns are estimates; measure with `forge test --gas-report` before optimizing.
- The vault in `TokenVault.t.sol` is intentionally simplified for teaching — it is not production-grade vault logic.
