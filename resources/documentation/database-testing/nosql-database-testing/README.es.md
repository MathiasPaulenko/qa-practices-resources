# Companion de Testing de Bases de Datos NoSQL

Checks ejecutables para la [guía de Testing de Bases de Datos NoSQL](https://qapractices.com/es/documentation/nosql-database-testing/) en qapractices.com: una suite de validación `$jsonSchema` de MongoDB, un script de aserciones sobre `explain()` y un test de consistencia de DynamoDB contra DynamoDB Local.

## Estructura

```text
nosql-database-testing/
├── mongo/
│   ├── schema-validation-tests.js   # Suite PASS/FAIL: inserciones válidas + 4 inválidas vs $jsonSchema
│   └── explain-check.js             # Siembra 5k pedidos, verifica IXSCAN + docs examinados acotados
├── dynamodb/
│   ├── consistency-test.js          # Aserciones de lectura strong vs eventual (AWS SDK v3)
│   └── package.json
└── meta.json
```

## Requisitos

- **MongoDB**: MongoDB 8 (o 7) local con `mongosh` — `docker run -d -p 27017:27017 mongo:8`
- **DynamoDB**: DynamoDB Local — `docker run -p 8000:8000 amazon/dynamodb-local` — más Node 18+

## Ejecutar los checks de MongoDB

```bash
mongosh mongodb://localhost:27017/nosql_test mongo/schema-validation-tests.js
```

Salida esperada:

```text
PASS  valid document
PASS  missing required field (createdAt): rejected (121)
PASS  invalid type (age as string): rejected (121)
PASS  role outside enum: rejected (121)
PASS  direct insert bypasses nothing: rejected (121)

5 passed, 0 failed
```

El último caso demuestra que la regla vive en la base de datos y no en el ORM: una inserción directa sin `email` es rechazada por el validador del servidor.

```bash
mongosh mongodb://localhost:27017/nosql_test mongo/explain-check.js
```

Salida esperada:

```text
customer + status + recent
  stage: IXSCAN | docsExamined: ~50 | nReturned: ~50 | time: ~1 ms
  PASS
customer + pending
  stage: IXSCAN | docsExamined: ~20 | nReturned: ~20 | time: ~1 ms
  PASS
```

Si algún plan muestra `NO INDEX`, el script sale con código distinto de cero — conéctalo en CI para detectar regresiones de índices.

## Ejecutar el test de consistencia de DynamoDB

```bash
cd dynamodb
npm install
docker run -d -p 8000:8000 amazon/dynamodb-local
node consistency-test.js
```

Salida esperada:

```text
strong read: PASS (value visible)
eventual read: PASS (tolerated)
```

Configura `DYNAMODB_ENDPOINT` para apuntar a otro endpoint local. La aserción de lectura eventual tolera valores obsoletos a propósito — contra DynamoDB real una lectura eventual inmediata puede ir retrasada; el test documenta la tolerancia esperada en lugar de exigir frescura que no puede garantizar.

## Notas

- El código de error `121` es el `DocumentValidationFailure` de MongoDB — la aserción acepta cualquier objeto de error, así que versiones más antiguas del servidor también pasan.
- Ambos scripts de mongosh llaman `quit(1)` al fallar, así que `echo $?` (o tu runner de CI) detecta regresiones sin parsear la salida.
