# Postman vs Insomnia — Runnable Companion

Artifacts from the ShopNext checkout decision in the [Postman vs Insomnia](https://qapractices.com/documentation/postman-vs-insomnia/) comparison on QAPractices.

## Contents

| Path | What it is |
|---|---|
| `postman/checkout-smoke-tests.js` | `pm.*` test script for the `POST /orders` request — status 201, `orderId` captured into a collection variable, response time under 400ms |
| `postman/newman-run.sh` | Newman 6 CLI invocation used in the CI step |
| `insomnia/grpc-inventory-test.js` | Insomnia 8.3 response test for `InventoryService.GetStock` (gRPC) |
| `ci/api-tests.yml` | GitHub Actions gate: checkout → Node 20 → Newman with cli+junit+htmlextra reporters → upload report artifact |
| `data/order-rows.csv` | Data rows for `newman run -d` |
| `data/staging.json` | Postman environment with `baseUrl` (placeholder staging host) |

## Usage

```bash
npm install -g newman newman-reporter-htmlextra
newman run collections/shopnext-checkout.json -e data/staging.json -d data/order-rows.csv --reporters cli,junit,htmlextra
```

The Postman collection itself is not included — export it from your own workspace and place it under `collections/`; the scripts and data files here plug straight into it. See the guide for the weighted decision matrix behind picking Postman + Newman as the CI backbone and keeping Insomnia for gRPC exploration.
