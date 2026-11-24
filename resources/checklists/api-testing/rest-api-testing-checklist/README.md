# REST API Testing Checklist — Companion

Executable companion for the [REST API Testing Checklist](https://qapractices.com/checklists/rest-api-testing-checklist): an HTTP contract prober plus a Newman smoke collection.

## Files

| File | What it does |
|------|--------------|
| `check_contract.py` | Probes one route for contract violations: wrong status classes, empty error bodies, missing `Allow`, non-idempotent `PUT`, unsafe repeat `DELETE`. Pure Python stdlib, no dependencies. |
| `sample_collection.json` | Postman/Newman collection skeleton — happy path + `401` + `404` per route, with status-first assertions. |

## Usage

```bash
# Contract probe against a live endpoint
python check_contract.py --base http://localhost:8080 --route /users/1 \
    --token $TOKEN --methods GET,PUT,DELETE

# Newman smoke run
newman run sample_collection.json --env-var base_url=http://localhost:8080 --env-var token=$TOKEN
```

`check_contract.py` exits `1` and lists violations when the route breaks the contract — wire it into CI as a smoke gate.
