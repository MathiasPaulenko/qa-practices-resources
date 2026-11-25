# Postman vs Insomnia — Companion Ejecutable

Artefactos de la decisión del checkout de ShopNext en la comparativa [Postman vs Insomnia](https://qapractices.com/es/documentation/postman-vs-insomnia/) de QAPractices.

## Contenido

| Ruta | Qué es |
|---|---|
| `postman/checkout-smoke-tests.js` | Script de test `pm.*` para el request `POST /orders` — status 201, `orderId` capturado en variable de colección, tiempo de respuesta bajo 400ms |
| `postman/newman-run.sh` | Invocación CLI de Newman 6 usada en el paso de CI |
| `insomnia/grpc-inventory-test.js` | Test de respuesta de Insomnia 8.3 para `InventoryService.GetStock` (gRPC) |
| `ci/api-tests.yml` | Puerta de GitHub Actions: checkout → Node 20 → Newman con reporters cli+junit+htmlextra → subir artefacto del reporte |
| `data/order-rows.csv` | Filas de datos para `newman run -d` |
| `data/staging.json` | Entorno de Postman con `baseUrl` (host de staging de placeholder) |

## Uso

```bash
npm install -g newman newman-reporter-htmlextra
newman run collections/shopnext-checkout.json -e data/staging.json -d data/order-rows.csv --reporters cli,junit,htmlextra
```

La colección de Postman en sí no está incluida — expórtala desde tu propio workspace y colócala bajo `collections/`; los scripts y datos de aquí enchufan directo. Mira la guía para la matriz de decisión ponderada detrás de elegir Postman + Newman como backbone de CI y mantener Insomnia para exploración gRPC.
