# Postman Test Scripts Cheat Sheet — Companion Resources

Companion resources for the [Postman Test Scripts Cheat Sheet](https://qapractices.com/documentation/postman-test-scripts-cheat-sheet/) on QAPractices.com. Every snippet in the article ships here inside a runnable collection — no real API or credentials needed: all requests target [postman-echo.com](https://postman-echo.com), Postman's own test API.

## Contents

| File | Description |
| --- | --- |
| `collections/postman-test-scripts.postman_collection.json` | 4 requests exercising the cheat sheet: basic assertions, JSON checks, token extraction + chaining, schema validation and a data-driven request. Includes a collection-level shared assertion. |
| `environments/staging.postman_environment.json` | Staging environment with `baseUrl=https://postman-echo.com`. |
| `data/users.csv` | 3-row dataset for the data-driven request (`name`, `email`, `quantity`) — use with the Collection Runner or Newman `-d`. |

## Requirements

- Postman v11 (GUI) or Newman 6.x (CLI)
- Node.js 20 LTS (for Newman)

## Quick Start

1. Open Postman v11 and click **Import**.
2. Select `collections/postman-test-scripts.postman_collection.json`.
3. Import `environments/staging.postman_environment.json` and pick **Staging** in the environment dropdown.
4. Run individual requests, or the whole collection with the Runner — for data-driven mode select `data/users.csv` as the data file.

## Run with Newman 6.x

```bash
npm install -g newman@6

# Whole collection
newman run collections/postman-test-scripts.postman_collection.json \
  -e environments/staging.postman_environment.json

# Data-driven run — the 4th request asserts each CSV row via pm.iterationData
newman run collections/postman-test-scripts.postman_collection.json \
  -e environments/staging.postman_environment.json \
  -d data/users.csv
```

Notes: emails in `users.csv` use the RFC 2606 reserved `.test` TLD — swap in your own domain for real runs. The token in "POST — Login" is a generated `{{$guid}}` echoed back by postman-echo, used only to demonstrate extraction and request chaining.
