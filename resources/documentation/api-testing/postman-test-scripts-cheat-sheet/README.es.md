# Postman Test Scripts: Cheat Sheet — Recursos Complementarios

Recursos complementarios del [Cheat Sheet de Postman Test Scripts](https://qapractices.com/es/documentation/postman-test-scripts-cheat-sheet/) en QAPractices.com. Cada snippet del artículo viene dentro de una colección ejecutable — sin API real ni credenciales: todos los requests apuntan a [postman-echo.com](https://postman-echo.com), la API de pruebas de Postman.

## Contenido

| Archivo | Descripción |
| --- | --- |
| `collections/postman-test-scripts.postman_collection.json` | 4 requests que ejercitan el cheat sheet: aserciones básicas, validación JSON, extracción de token + encadenamiento, validación de schema y un request data-driven. Incluye una aserción compartida a nivel de colección. |
| `environments/staging.postman_environment.json` | Entorno staging con `baseUrl=https://postman-echo.com`. |
| `data/users.csv` | Dataset de 3 filas para el request data-driven (`name`, `email`, `quantity`) — usar con el Collection Runner o Newman `-d`. |

## Requisitos

- Postman v11 (GUI) o Newman 6.x (CLI)
- Node.js 20 LTS (para Newman)

## Inicio Rápido

1. Abre Postman v11 y haz clic en **Import**.
2. Selecciona `collections/postman-test-scripts.postman_collection.json`.
3. Importa `environments/staging.postman_environment.json` y elige **Staging** en el desplegable de entornos.
4. Ejecuta requests individuales o la colección completa con el Runner — para modo data-driven selecciona `data/users.csv` como archivo de datos.

## Ejecutar con Newman 6.x

```bash
npm install -g newman@6

# Colección completa
newman run collections/postman-test-scripts.postman_collection.json \
  -e environments/staging.postman_environment.json

# Ejecución data-driven — el 4.º request aserta cada fila CSV vía pm.iterationData
newman run collections/postman-test-scripts.postman_collection.json \
  -e environments/staging.postman_environment.json \
  -d data/users.csv
```

Notas: los emails de `users.csv` usan el TLD `.test` reservado por RFC 2606 — cámbialos por tu dominio para ejecuciones reales. El token de "POST — Login" es un `{{$guid}}` generado que postman-echo devuelve, usado solo para demostrar extracción y encadenamiento de requests.
