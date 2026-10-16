# Prompt de IA: Casos de Test de Smart Contracts — Companion

Archivos companion del recurso [Prompt de IA: Casos de Test de Smart Contracts](https://qapractices.com/es/prompts/ai-prompt-blockchain-smart-contract-test-cases/).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El template del prompt completo, listo para copiar en cualquier LLM (en inglés; la versión española del recurso muestra la traducción). |
| `example-input.txt` | Entrada de ejemplo rellenada: un contrato TokenVault estilo ERC4626 en Solidity ^0.8.24 detrás de un proxy UUPS. |
| `TokenVault.t.sol` | Archivo de test de Foundry ejecutable — el tipo de salida que el prompt debería producir: correctitud de deposit/withdraw, reverts de frontera, un intento de reentrancia (SWC-107) con contrato atacante auxiliar, control de acceso y checks de pausa. |

## Uso

1. Copia `prompt-template.txt` en tu LLM (ChatGPT, Claude, asistentes tipo Copilot).
2. Reemplaza los placeholders entre corchetes con el contexto de tu contrato — o ejecútalo tal cual contra `example-input.txt`.
3. Compara los casos generados con `TokenVault.t.sol` para verificar formato y profundidad: cada caso debería mapear a una función de test real.
4. Para correr la suite de ejemplo: `forge init --no-git vault-test`, copia `TokenVault.t.sol` en `test/`, `forge install OpenZeppelin/openzeppelin-contracts`, luego `forge test`.

## Requisitos

- Cualquier LLM para el prompt en sí.
- [Foundry](https://book.getfoundry.sh/) (`forge`) y OpenZeppelin Contracts 5.x para correr `TokenVault.t.sol`.

## Prompts de seguimiento

Después de generar los casos de test, continúa la conversación con:

- "Convierte estos casos de test en un archivo de test de Foundry completo — setup, fixtures y el contrato atacante incluidos."
- "Escribe una suite de invariantes para este contrato: lista las propiedades que deben cumplirse siempre (totalSupply igual a la suma de balances, el vault no puede pagar más de lo que tiene) como invariant tests de forge."
- "Genera una configuración de fuzzing de Foundry para el round-trip deposit/withdraw: cantidad de corridas, límites de entrada y las propiedades a verificar."
- "Produce una configuración de Slither 0.10.x más una checklist de triage que separe los hallazgos que importan del ruido."

## Notas

- Los casos de test generados son un andamiaje, no cobertura de auditoría — revísalos antes de confiar en la suite.
- Nunca pegues claves privadas, seed phrases ni direcciones de mainnet con fondos en el prompt.
- Los números de gas que devuelve el modelo son estimaciones; mide con `forge test --gas-report` antes de optimizar.
- El vault de `TokenVault.t.sol` está simplificado a propósito con fines didácticos — no es lógica de vault de producción.
