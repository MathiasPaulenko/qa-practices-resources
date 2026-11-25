#!/usr/bin/env bash
# Problem 5 — split the suite across 4 GitHub Actions runners (Playwright sharding)
# matrix.shard = 1..4, matrix.total = 4
npx playwright test --shard=${{ matrix.shard }}/${{ matrix.total }}
