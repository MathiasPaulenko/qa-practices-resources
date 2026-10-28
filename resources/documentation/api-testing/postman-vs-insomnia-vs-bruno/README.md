# Postman vs Insomnia vs Bruno — Runnable Companion

Companion for the [Postman vs Insomnia vs Bruno decision guide](https://qapractices.com/documentation/postman-vs-insomnia-vs-bruno/) on QAPractices.

This repo holds the checkout contract-test suite exactly as described in the article, in both formats so you can compare the Git-diff experience yourself:

```text
api-tests/checkout/          Bruno collection (4 chained requests)
├── bruno.json
├── create-cart.bru          seq 1 — saves cartId via vars:post-response
├── add-item.bru             seq 2 — reads cartId
├── checkout.bru             seq 3 — saves transactionId
├── refund.bru               seq 4 — partial refund, <600ms assertion
└── environments/
    └── staging.bru          baseUrl + secret authToken slot
postman/
└── checkout-contract.postman_collection.json   same 4 requests, pm.test + pm.environment chaining
.github/workflows/
└── api-contract-tests.yml   runs bru run and newman run on every PR
```

## Run it

```bash
# Bruno (2.x) — the repo is the source of truth
npm install -g @usebruno/cli@2.13.0
bru run api-tests/checkout --env staging --output results.json

# Newman (6.x) — needs the exported JSON
npm install -g newman@6.2.1
newman run postman/checkout-contract.postman_collection.json
```

## Notes

- `environments/staging.bru` declares `authToken` as a `vars:secret` entry — provide the real value via `PAYFUSE_STAGING_TOKEN` (CI) or a local env override; never commit it.
- The base URL `staging.payfuse.internal` is a placeholder — point it at your own staging API.
- Newman runs the exported collection JSON; keep it in sync with the Postman workspace or diffs will drift.
