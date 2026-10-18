# Casos de Prueba de Transacciones Blockchain — Companion

Companion ejecutable de los [Casos de Prueba de Transacciones Blockchain](https://qapractices.com/es/test-cases/blockchain-transaction-test-cases).

## Contenido

| Archivo | Descripción |
|---|---|
| `hardhat-transaction.test.js` | Suite Hardhat 2.22 + ethers 6.x que cubre TC-01, TC-02, TC-06, TC-12 y TC-19 |
| `GuardedVault.sol` | Contrato mínimo con `onlyOwner` usado por el test de autorización (TC-19) |

## Uso

```bash
npm install --save-dev hardhat @nomicfoundation/hardhat-ethers ethers chai
npx hardhat init # o suelta estos archivos en un proyecto hardhat existente
cp GuardedVault.sol contracts/
npx hardhat test hardhat-transaction.test.js
```

Para los casos edge que necesitan control de cadena (gaps de nonce, reorgs, minado manual), corre contra Anvil:

```bash
anvil --no-mining   # envía las txs, luego mina manualmente para observar el estado pending
```
