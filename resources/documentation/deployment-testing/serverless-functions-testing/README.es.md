# Testing de Funciones Serverless — Companion

Companion ejecutable de la guía [Cómo Probar Funciones Serverless: AWS Lambda, Azure](https://qapractices.com/es/documentation/serverless-functions-testing).

Una función Lambda `GET /orders/{id}` respaldada por DynamoDB, con todo lo necesario para ejercitar las tres capas de testing de la guía:

- `template.yaml` — plantilla SAM: función `nodejs22.x`, política `DynamoDBReadPolicy` de privilegio mínimo, evento de API Gateway y la definición de la tabla.
- `src/handler.mjs` — el handler bajo prueba.
- `events/get-order.json` — evento sintético de API Gateway para invocación local.
- `env.json` — variables de entorno para `sam local`.
- `tests/handler.test.mjs` — pruebas unitarias con Jest 30 y `aws-sdk-client-mock`, sin necesidad de credenciales de AWS.

## Ejecutar las pruebas unitarias

```bash
npm install
npm test
```

## Invocar la función localmente

Requiere AWS SAM CLI 1.172 y Docker en ejecución:

```bash
sam build && sam local invoke OrdersFunction \
  --event events/get-order.json \
  --env-vars env.json
```

`sam local` ejecuta el handler pero no DynamoDB: para un recorrido local completo, apunte el endpoint del SDK a LocalStack 2026.10 o despliegue a una cuenta de prueba con `sam deploy --guided`.
