# Companion de REST Assured vs Karate vs Axios

Recurso complementario de la comparativa [REST Assured vs Karate vs Axios](https://qapractices.com/es/documentation/rest-assured-vs-karate-vs-axios). Implementa el mismo escenario — `GET /users/1` más un camino negativo 404 contra [JSONPlaceholder](https://jsonplaceholder.typicode.com) — en las tres librerías para comparar sintaxis, coste de setup y salida lado a lado.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `rest-assured/pom.xml` | Configuración Maven con REST Assured 5.5.7, JUnit 5.11.4, Hamcrest 3.0 |
| `rest-assured/src/test/java/com/qapractices/UserApiTest.java` | Clase de test JUnit 5 con assertions de DSL fluido |
| `karate/users-api.feature` | Escenarios Gherkin con assertions `match` y `karate-config.js` |
| `karate/karate-config.js` | Configuración de entorno (`baseUrl` sobrescribible con `-DbaseUrl=...`) |
| `axios/package.json` | Proyecto Node con Axios 1.20.x y Jest 30 |
| `axios/user-api.test.js` | Test Jest con una instancia Axios compartida (`baseURL` + headers por defecto) |

## Inicio Rápido

### REST Assured

```bash
cd rest-assured
mvn clean test
```

Requiere Java 17+ y Maven 3.9+.

### Karate

Descarga el JAR standalone desde la [página de releases de Karate](https://github.com/karatelabs/karate/releases) y ejecuta:

```bash
java -jar karate.jar users-api.feature
```

O integra el feature en un proyecto Maven/Gradle con la dependencia `io.karatelabs:karate-junit5`.

### Axios

```bash
cd axios
npm install
npm test
```

Requiere Node.js 20+.

## Qué comparar

- **Líneas de setup**: REST Assured necesita un `pom.xml` e imports; Karate necesita un feature más `karate-config.js`; Axios necesita `npm install` y un runner de pruebas.
- **Estilo de assertions**: matchers fluidos `.body(...)` vs `match` de Karate vs `expect` de Jest.
- **Reportes**: REST Assured reporta vía Surefire/Allure, Karate genera reportes HTML automáticamente, los tests de Axios reportan a través de Jest.
- **Paralelismo**: Karate ejecuta escenarios en paralelo por defecto; las otras dos necesitan configuración a nivel de runner.
