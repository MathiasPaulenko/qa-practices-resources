# REST Assured vs Postman: la misma suite de API en ambas herramientas

Complemento de la guía de QAPractices [REST Assured vs Postman: Comparación para API Testing](https://qapractices.com/es/documentation/rest-assured-vs-postman/).

Los mismos tres chequeos de API —GET por id, falta de API key devuelve 401, respuesta en menos de 2s— implementados dos veces: una como suite JUnit 5 con REST Assured 5.x, otra como colección de Postman que Newman 6.x puede correr headless. Compara ambas formas lado a lado.

## Estructura del proyecto

```text
rest-assured/
├── pom.xml
└── src/test/java/com/qapractices/api/
    └── UserApiTest.java
postman/
├── users-collection.postman_collection.json
└── env-dev.postman_environment.json
```

## Mapeo de conceptos

| REST Assured | Postman/Newman | Notas |
|--------------|----------------|-------|
| `given()/when()/then()` | `pm.test()` + `pm.expect` | Mismo flujo request-assert, sintaxis distinta |
| `System.getProperty("api.url")` | variable `{{baseUrl}}` de entorno | Ambos externalizan el entorno destino |
| `System.getenv("API_KEY")` | variable `{{apiKey}}` de entorno | Nunca commitees claves reales — usa variables |
| `mvn test` | `newman run collection.json -e env.json` | REST Assured corre dentro del build; Newman necesita un JSON exportado |
| JUnit XML (Surefire) | `newman --reporters cli,junit` | Ambos alimentan los reportes de CI |

## Requisitos

- Lado REST Assured: JDK 17+, Maven 3.9+.
- Lado Postman: Newman 6.x (`npm install -g newman`) o la app de Postman para importar la colección.

## Uso

```bash
# REST Assured
cd rest-assured && API_KEY=tu-clave mvn test

# Postman via Newman
cd postman && newman run users-collection.postman_collection.json \
  -e env-dev.postman_environment.json --reporters cli,junit
```

Apunta `api.url` / `{{baseUrl}}` a una API real — el `api.acme-retail.com` por defecto es un placeholder para un servicio local o de staging.
