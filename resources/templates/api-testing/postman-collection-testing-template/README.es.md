# Plantilla de Testing de Colecciones Postman — Companion

Archivos ejecutables que implementan la [plantilla Testing de Colecciones Postman: Newman](https://qapractices.com/es/templates/postman-collection-testing-template/) de QAPractices: una colección exportada con scripts de aserción `pm.test`, un entorno de staging, un archivo CSV para ejecuciones basadas en datos y un workflow de GitHub Actions.

## Archivos

| Archivo | Qué es |
|---|---|
| `api-test-collection.postman_collection.json` | Export de Postman Collection v2.1: carpeta de auth, carpeta de users, tests negativos, scripts `pm.test` |
| `staging.postman_environment.json` | Variables del entorno de staging — reemplaza las credenciales placeholder antes de ejecutar |
| `login_test_data.csv` | Archivo de datos para el test de login basado en datos (7 filas: casos válidos, inválidos y límite) |
| `newman-ci.yml` | Workflow de GitHub Actions que instala Newman 6.x y ejecuta la colección con reporte htmlextra |

## Ejecutarlo

```bash
npm install -g newman@6 newman-reporter-htmlextra@1

newman run api-test-collection.postman_collection.json \
  -e staging.postman_environment.json \
  -d login_test_data.csv \
  -r cli,htmlextra \
  --reporter-htmlextra-export reports/api-test-report.html
```

La colección apunta `{{base_url}}` a tu API de staging. Sobrescríbela sin editar archivos:

```bash
newman run api-test-collection.postman_collection.json \
  -e staging.postman_environment.json \
  --env-var "base_url=https://api.staging.tu-dominio.com"
```

## Notas

- El request `Login_Valid` escribe `auth_token` y `refresh_token` en el entorno desde su script de test; los requests siguientes consumen `{{auth_token}}`.
- `newman-ci.yml` espera la colección en `collections/` y el entorno en `environments/` — ajusta las rutas a tu repo.
- Newman sale con código distinto de cero si falla cualquier aserción, así que el workflow falla el job automáticamente.

Fuente: [qapractices.com/es/templates/postman-collection-testing-template](https://qapractices.com/es/templates/postman-collection-testing-template/)
