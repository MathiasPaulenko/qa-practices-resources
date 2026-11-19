# Plantilla de Testing de Smart Contracts Blockchain — Companion

Archivos descargables de la [Plantilla de Testing de Smart Contracts Blockchain](https://qapractices.com/es/templates/blockchain-smart-contract-testing-template/) de QAPractices.

## Contenido

| Archivo | Propósito |
|---|---|
| `smart-contract-testing-log.md` | Documento de testing en blanco con las once secciones: datos del contrato, entorno de test, cobertura unitaria, control de acceso, presupuesto de gas, checklist de vulnerabilidades, tests de upgrade, integración, verificación de deployment, seguimiento de defectos y sign-off. |
| `smart-contract-testing-log-sample.md` | El mismo documento completado para un ERC-20 pausable ficticio llamado SAFE en Polygon, testeado con Foundry antes de una auditoría externa. |

## Uso

1. Copia `smart-contract-testing-log.md` a la documentación, wiki o repo de tu proyecto.
2. Completa primero los Detalles del Contrato — la red, la versión de Solidity y el framework definen qué herramientas aplican después.
3. Saca el conteo de tests de la salida de `forge test` o `npx hardhat test`, nunca de memoria.
4. Registra cada fallo en Seguimiento de Defectos con su severidad antes de corregirlo; los auditores trazan cada SC-xxx hasta el commit que lo resolvió.
5. Reúne las aprobaciones solo cuando la verificación de deployment pase sobre la red real.

Usa `smart-contract-testing-log-sample.md` como referencia de nivel de detalle y valores realistas.
