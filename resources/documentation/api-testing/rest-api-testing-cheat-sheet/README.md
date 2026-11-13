# REST API Testing Cheat Sheet — Companion

Runnable companion for the [REST API Testing Cheat Sheet](https://qapractices.com/documentation/rest-api-testing-cheat-sheet/) on QAPractices.com.

## Contents

- `requests.http` — the full per-method pass from the cheat sheet: GET (with filters and a 404 negative), POST, PUT, PATCH, DELETE, HEAD, OPTIONS, three auth header variants, and four security probes (missing auth, SQLi, XSS, path traversal).

## How to run

Any `.http` client works:

- **VS Code** — install the REST Client extension, open `requests.http`, click "Send Request" above each block.
- **JetBrains IDEs** — open the file and run each request from the gutter icon.
- **Postman** — import the file (Postman reads `.http`/`.rest` collections).
- **curl** — each block maps 1:1 to a curl command; the bash version of the CRUD pass is in the article's "Practical Example" section.

## Target

Requests default to `https://jsonplaceholder.typicode.com`, a public test API that accepts writes without persisting them. Change `@baseUrl` to your staging API to run the same pass against a real service — the security probes only make sense against an API you own.
