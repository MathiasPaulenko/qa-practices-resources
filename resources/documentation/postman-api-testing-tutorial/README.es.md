# Tutorial de Postman API Testing — Recursos Complementarios

Recursos complementarios para el [Tutorial de Postman API Testing](https://qapractices.com/es/documentation/postman-api-testing-tutorial/) en QAPractices.com.

## Contenido

| Archivo | Descripción |
| --- | --- |
| `collections/user-api-tests.postman_collection.json` | Colección de Postman con requests GET, POST, login y encadenados. Incluye test scripts con assertions. |
| `environments/staging.postman_environment.json` | Entorno de staging con `baseUrl`, `apiToken`, `userId` y variables de autenticación. |
| `data/test-data.json` | Datos para testing data-driven con el flag `-d` de Newman. |

## Requisitos

- Postman v11 (GUI) o Newman 6.x (CLI)
- Node.js 20 LTS

## Inicio Rápido

Importá la colección y el entorno en Postman:

1. Abrí Postman v11
2. Hacé clic en **Import** y seleccioná `collections/user-api-tests.postman_collection.json`
3. Hacé clic en **Import** de nuevo y seleccioná `environments/staging.postman_environment.json`
4. Seleccioná el entorno **Staging** desde el dropdown
5. Corré requests individuales o la colección completa

## Correr con Newman (CLI)

```bash
# Instalar Newman 6.x
npm install -g newman
npm install -g newman-reporter-htmlextra

# Correr la colección con el entorno de staging
newman run collections/user-api-tests.postman_collection.json \
  -e environments/staging.postman_environment.json \
  --reporters cli,htmlextra

# Correr con datos de testing data-driven
newman run collections/user-api-tests.postman_collection.json \
  -e environments/staging.postman_environment.json \
  -d data/test-data.json \
  --reporters cli,htmlextra
```

## Integración con CI/CD (GitHub Actions)

```yaml
name: API Tests
on: [push, pull_request]
jobs:
  postman-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Install Newman
        run: |
          npm install -g newman
          npm install -g newman-reporter-htmlextra
      - name: Run Postman Collection
        run: |
          newman run collections/user-api-tests.postman_collection.json \
            -e environments/staging.postman_environment.json \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export reports/report.html
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: postman-report
          path: reports/
```

## Recursos Relacionados

- [Tutorial de Postman API Testing](https://qapractices.com/es/documentation/postman-api-testing-tutorial/)
- [Guía de REST Assured API Testing](https://qapractices.com/es/documentation/rest-assured-api-testing-guide/)
- [Guía de API Testing](https://qapractices.com/es/documentation/api-testing-guide/)
