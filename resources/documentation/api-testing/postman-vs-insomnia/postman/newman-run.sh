#!/usr/bin/env bash
# Run the checkout suite in CI with Newman 6
newman run shopnext-checkout.json -e staging.json -d order-rows.csv --reporters cli,junit
