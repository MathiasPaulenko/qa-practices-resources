# REST Assured vs Postman: Same API Suite in Both Tools

Companion to the QAPractices guide [REST Assured vs Postman: API Testing Comparison](https://qapractices.com/documentation/rest-assured-vs-postman/).

The same three API checks — GET by id, missing API key returns 401, response under 2s — implemented twice: once as a REST Assured 5.x JUnit 5 suite, once as a Postman collection that Newman 6.x can run headless. Compare the two shapes side by side.

## Project structure

```text
rest-assured/
├── pom.xml
└── src/test/java/com/qapractices/api/
    └── UserApiTest.java
postman/
├── users-collection.postman_collection.json
└── env-dev.postman_environment.json
```

## Concept mapping

| REST Assured | Postman/Newman | Notes |
|--------------|----------------|-------|
| `given()/when()/then()` | `pm.test()` + `pm.expect` | Same request-assert flow, different syntax |
| `System.getProperty("api.url")` | `{{baseUrl}}` environment variable | Both externalize the target environment |
| `System.getenv("API_KEY")` | `{{apiKey}}` environment variable | Never commit real keys — use env vars |
| `mvn test` | `newman run collection.json -e env.json` | REST Assured runs inside your build; Newman needs an exported JSON |
| JUnit XML (Surefire) | `newman --reporters cli,junit` | Both feed CI reports |

## Requirements

- REST Assured side: JDK 17+, Maven 3.9+.
- Postman side: Newman 6.x (`npm install -g newman`) or the Postman app to import the collection.

## Usage

```bash
# REST Assured
cd rest-assured && API_KEY=your-key mvn test

# Postman via Newman
cd postman && newman run users-collection.postman_collection.json \
  -e env-dev.postman_environment.json --reporters cli,junit
```

Point `api.url` / `{{baseUrl}}` at a real API — the default `api.acme-retail.com` is a placeholder for a local or staging service.
