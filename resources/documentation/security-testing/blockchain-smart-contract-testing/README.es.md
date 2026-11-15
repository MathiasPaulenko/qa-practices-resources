# Testing de Smart Contracts en Blockchain — Ejemplo con Foundry

Un proyecto Foundry mínimo y ejecutable usado en la guía de QAPractices:

- [Guía de Testing de Blockchain y Smart Contracts](https://qapractices.com/es/documentation/blockchain-smart-contract-testing-guide/)

Cubre los patrones de test que recomienda la guía: tests unitarios, fuzz tests,
condiciones de revert, assertions de eventos y un contrato atacante de reentrancy
que demuestra que el orden checks-effects-interactions del vault realmente protege
los fondos.

## Setup

```bash
# Instalar Foundry (forge, cast, anvil)
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Instalar dependencias (forge-std)
forge install foundry-rs/forge-std --no-commit
```

## Ejecutar

```bash
forge test                      # suite completa
forge test -vvv                 # trazas detalladas
forge test --gas-report         # tabla de gas por función
forge snapshot                  # escribe .gas-snapshot para diffs en CI
forge test --fork-url $MAINNET_RPC_URL   # correr contra un fork de mainnet
```

## Estructura del proyecto

```text
├── foundry.toml                  # solc 0.8.24, runs de fuzz para el perfil CI
├── src/
│   └── SimpleVault.sol           # vault de depósito/retiro (checks-effects-interactions)
├── test/
│   ├── SimpleVault.t.sol         # tests unitarios, fuzz, revert y eventos
│   └── ReentrancyExploit.t.sol   # receptor malicioso que falla al re-ingresar
└── .github/workflows/foundry.yml # CI: build + test + gas snapshot
```

## Qué demuestran los tests

| Archivo de test | Patrón |
|---|---|
| `testDepositUpdatesBalance` | camino feliz + `vm.prank` + `vm.deal` |
| `testWithdrawInsufficientBalanceReverts` | `vm.expectRevert` en una condición de revert |
| `testDepositEmitsEvent` | assertion de evento con `vm.expectEmit` |
| `testFuzz_DepositWithinBalance` | fuzzing de inputs con `vm.assume` |
| `testFuzz_WithdrawNeverExceedsDeposit` | fuzz estilo propiedad sobre un camino de revert |
| `testReentrantWithdrawFails` | contrato atacante re-ingresando a `withdraw` — falla porque el estado queda en cero primero |

Salida esperada (truncada):

```text
[PASS] testDepositEmitsEvent() (gas: 42581)
[PASS] testDepositUpdatesBalance() (gas: 58732)
[PASS] testFuzz_DepositWithinBalance(uint96) (runs: 256)
[PASS] testReentrantWithdrawFails() (gas: 210445)
[PASS] testWithdrawInsufficientBalanceReverts() (gas: 13872)
```
