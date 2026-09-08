# Testing de Contratos API con Pact — Scripts Companion

> Recurso companion de [Testing de Contratos API con Pact: Contratos](https://qapractices.com/es/documentation/api-contract-testing-with-pact) en QAPractices.com.

Scripts para contract testing consumer-driven con Pact JS 13.x y Pact Python 2.x. Incluye tests de consumidor, verificación de provider, scripts de publicación, checks can-i-deploy y un workflow de CI/CD.

## Requisitos

- Node.js 20+
- npm 10+
- `@pact-foundation/pact` 13.x
- Python 3.12+ (para ejemplos en Python)
- `pact-python` 2.x (para ejemplos en Python)
- Un Pact Broker corriendo (ej. `https://pact-broker.qa.local`)

## Setup

```bash
# Clonar e instalar
npm init -y
npm install @pact-foundation/pact@13 @pact-foundation/pact-node@14

# Para ejemplos en Python
pip install pact-python==2.* requests==2.32

# Correr tests de consumidor
npm run test:consumer

# Correr verificación de provider
npm run test:provider

# Publicar pacts al broker
node scripts/publish-pacts.js

# Check Can-I-Deploy
pact-broker can-i-deploy \
  --pacticipant UserService \
  --version 2.4.1 \
  --to-environment production \
  --broker-base-url https://pact-broker.qa.local \
  --broker-token $PACT_TOKEN
```

## Archivos

| Archivo | Propósito |
| --------- | ----------- |
| `scripts/consumer.test.js` | Test de contrato de consumidor con PactV3 |
| `scripts/provider.test.js` | Verificación de provider contra API real |
| `scripts/publish-pacts.js` | Publicar archivos Pact al broker |
| `scripts/python_consumer_test.py` | Test de consumidor en Python con pact-python 2.x |
| `scripts/can-i-deploy-consumer.sh` | Check Can-I-Deploy para un consumidor |
| `scripts/cli-provider-verify.sh` | Verificación de provider por CLI con pact-verifier |
| `.github/workflows/contract-tests.yml` | Workflow de CI/CD para jobs de consumer + provider |

## Arquitectura

Los scripts siguen el flujo de contract testing:

1. El test de consumidor genera un archivo Pact (artefacto JSON).
2. El archivo Pact se publica al Pact Broker.
3. El provider obtiene los contratos del broker y verifica contra la API real.
4. Los resultados de verificación se publican de vuelta al broker.
5. `can-i-deploy` consulta al broker antes de cualquier despliegue.

## Licencia

MIT — libre de usar, modificar y distribuir.
