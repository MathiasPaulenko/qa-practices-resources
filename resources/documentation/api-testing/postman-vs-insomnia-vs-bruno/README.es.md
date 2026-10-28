# Postman vs Insomnia vs Bruno — Companion ejecutable

Companion de la [guía de decisión Postman vs Insomnia vs Bruno](https://qapractices.com/es/documentation/postman-vs-insomnia-vs-bruno/) en QAPractices.

Este repo contiene la suite de tests de contrato de checkout tal como la describe el artículo, en los dos formatos para que compares la experiencia de `git diff` vos mismo:

```text
api-tests/checkout/          Colección Bruno (4 requests encadenados)
├── bruno.json
├── create-cart.bru          seq 1 — guarda cartId vía vars:post-response
├── add-item.bru             seq 2 — lee cartId
├── checkout.bru             seq 3 — guarda transactionId
├── refund.bru               seq 4 — reembolso parcial, aserción <600ms
└── environments/
    └── staging.bru          baseUrl + slot secreto para authToken
postman/
└── checkout-contract.postman_collection.json   mismos 4 requests, encadenamiento con pm.test + pm.environment
.github/workflows/
└── api-contract-tests.yml   corre bru run y newman run en cada PR
```

## Ejecución

```bash
# Bruno (2.x) — el repo es la fuente de verdad
npm install -g @usebruno/cli@2.13.0
bru run api-tests/checkout --env staging --output results.json

# Newman (6.x) — necesita el JSON exportado
npm install -g newman@6.2.1
newman run postman/checkout-contract.postman_collection.json
```

## Notas

- `environments/staging.bru` declara `authToken` como `vars:secret`: pasá el valor real vía `PAYFUSE_STAGING_TOKEN` (CI) o un override de entorno local; nunca lo commitees.
- La URL base `staging.payfuse.internal` es un placeholder — apuntala a tu propia API de staging.
- Newman corre el JSON de colección exportado; mantenelo sincronizado con el workspace de Postman o los diffs van a divergir.
