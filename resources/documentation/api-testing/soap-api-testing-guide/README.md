# SOAP API Testing Guide — Companion

Runnable SOAP testing fixtures: WSDL validation script, XML request template, XSD schema, curl command, SoapUI Groovy assertion and GitHub Actions workflow for the [SOAP API Testing Guide](https://qapractices.com/documentation/soap-api-testing-guide/).

## Contents

| File | What it does |
| --- | --- |
| `request.xml` | SOAP 1.1 envelope template for an AuthorizePayment request |
| `payment.xsd` | XSD schema for validating SOAP responses |
| `validate-wsdl.sh` | Shell script that validates a WSDL with Apache CXF wsdl2java and xmllint |
| `soapui-groovy-assertion.groovy` | Groovy assertion for SoapUI that checks response elements with XPath |
| `.github/workflows/soap-tests.yml` | GitHub Actions workflow that runs wsdl2java and tests on every push |

## Quick Start

```bash
# 1. Validate the WSDL
./validate-wsdl.sh https://staging.example.com/payment?wsdl

# 2. Send a SOAP request with curl
curl -X POST \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: http://example.com/payment/AuthorizePayment" \
  --data @request.xml \
  https://staging.example.com/payment

# 3. Validate the response against the XSD
xmllint --schema payment.xsd response.xml --noout

# 4. Import the Groovy assertion into SoapUI
#    Add it as a Groovy Script assertion on your test step
```

## CI

The `.github/workflows/soap-tests.yml` file runs `cxf-codegen:wsdl2java` and tests on every push and pull request. The wsdl2java goal fails at compile time when the WSDL changes in a breaking way — contract drift becomes a build failure.

## License

MIT — see the main repository for details.
