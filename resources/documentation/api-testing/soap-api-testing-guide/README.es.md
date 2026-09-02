# Companion de la Guía de Testing de APIs SOAP

Fixtures ejecutables de testing SOAP: script de validación WSDL, template de request XML, schema XSD, comando curl, assertion Groovy de SoapUI y workflow de GitHub Actions para la [Guía de Testing de APIs SOAP](https://qapractices.com/es/documentation/soap-api-testing-guide/).

## Contenidos

| Archivo | Qué hace |
| --- | --- |
| `request.xml` | Template de envelope SOAP 1.1 para un request AuthorizePayment |
| `payment.xsd` | Schema XSD para validar respuestas SOAP |
| `validate-wsdl.sh` | Script shell que valida un WSDL con Apache CXF wsdl2java y xmllint |
| `soapui-groovy-assertion.groovy` | Assertion Groovy para SoapUI que chequea elementos del response con XPath |
| `.github/workflows/soap-tests.yml` | Workflow de GitHub Actions que ejecuta wsdl2java y tests en cada push |

## Quick Start

```bash
# 1. Validar el WSDL
./validate-wsdl.sh https://staging.example.com/payment?wsdl

# 2. Mandar un request SOAP con curl
curl -X POST \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: http://example.com/payment/AuthorizePayment" \
  --data @request.xml \
  https://staging.example.com/payment

# 3. Validar la respuesta contra el XSD
xmllint --schema payment.xsd response.xml --noout

# 4. Importar la assertion Groovy en SoapUI
#    Agregala como assertion de Groovy Script en tu test step
```

## CI

El archivo `.github/workflows/soap-tests.yml` ejecuta `cxf-codegen:wsdl2java` y tests en cada push y pull request. El goal wsdl2java falla en compile time cuando el WSDL cambia de forma breaking — el contract drift se convierte en un build failure.

## Licencia

MIT — ver el repositorio principal para detalles.
