# SOAP API Testing with Postman — Companion

Runnable fixtures for the QAPractices guide [SOAP API Testing with Postman](https://qapractices.com/documentation/soap-api-testing-postman/).

The collection hits `NumberConversion` at `www.dataaccess.com`, a free public SOAP demo service, so every example runs end to end without your own backend. Swap the endpoint and operation for your staging WSDL when you're ready.

## Files

| File | What it is |
|---|---|
| `numberconversion-soap.postman_collection.json` | Postman v11 collection: happy path with xml2Json assertions, a fault-triggering request and a WS-Security UsernameToken template |
| `soap-demo.postman_environment.json` | Environment with `ubiNum`, `soap_endpoint` and placeholder credentials |
| `run-newman.sh` | Newman 6.x run with `cli,junit` reporters and JUnit export |

## Usage

### In Postman

1. Import `numberconversion-soap.postman_collection.json` (**File → Import → File**).
2. Import `soap-demo.postman_environment.json` and select it as the active environment.
3. Run **NumberToWords — happy path**. All five tests should pass.
4. Run **NumberToWords — missing element triggers fault** to see a `soap:Fault` asserted correctly.

### With Newman 6.x

```bash
./run-newman.sh
```

The JUnit report lands in `results/soap-tests.xml`, ready for Jenkins, GitHub Actions or Azure DevOps test reporting. To wire it into your pipeline, run the script as a job step after deploying your service.

### Data-driven runs

Create a CSV with an `ubiNum` column and pass it to Newman:

```bash
newman run numberconversion-soap.postman_collection.json \
  --environment soap-demo.postman_environment.json \
  --iteration-data boundary-values.csv
```

The pre-request script picks up each row via `pm.iterationData`.

## Notes

- `{{soap_username}}` and `{{soap_password}}` ship as `replace-me` placeholders — the public demo ignores them. Point `soap_endpoint` at your service and fill in real credentials in a private environment, never in this file.
- For SOAP 1.2 services change `Content-Type` to `application/soap+xml` and move the action into the content type — see the guide's FAQ.
