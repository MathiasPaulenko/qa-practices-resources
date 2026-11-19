# API Versioning Testing Strategy Companion

Companion to the [API Versioning Testing Strategy](https://qapractices.com/documentation/api-versioning-testing-strategy/) guide on QAPractices.

## Files

- `compare-api-versions.sh` — fires identical requests at `v1` and `v2` of the same paths and diffs the responses, the cheapest breaking-change detector from the guide.

## Usage

```bash
chmod +x compare-api-versions.sh
./compare-api-versions.sh https://staging.example.com/api users/42 orders/1001
```

For every path, the script prints the unified diff between the `v1` and `v2` responses. Classify each change as breaking (rename, removal, type change) or additive (new field, new enum value) — and remember that "additive" still breaks clients with strict schema validation.

Promote the same request pairs into CI once the diff is stable; for consumer-driven coverage of the same checks, see the guide's Pact section.
