# Plantilla de Configuración de API Mock Server — Archivos Companion

Companion ejecutable de la [Plantilla de Configuración de API Mock Server](https://qapractices.com/es/templates/api-mock-server-setup-template). Incluye mappings de WireMock 3.13.2, un setup de Docker Compose y handlers de MSW 2.x para los endpoints de muestra `/users` más un escenario de inyección de fallos.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `docker-compose.yml` | Contenedor standalone de WireMock 3.13.2 en el puerto 3001 con mappings montados por volumen. |
| `mappings/get-user-by-id.json` | Happy path de `GET /users/{id}` (200) usando patrón de URL path. |
| `mappings/get-user-404.json` | `GET /users/99999` devuelve 404 con body de error. |
| `mappings/post-users.json` | `POST /users` devuelve 201 con simulación de latencia `fixedDelayMs`. |
| `mappings/get-users-rate-limited.json` | `GET /users` con header `X-Simulate-Latency` devuelve una respuesta lenta de 5 segundos (ejemplo de inyección de fallos). |
| `msw/handlers.js` | Handlers de MSW 2.x para los mismos endpoints, para suites de test en Node/navegador. |

## Uso

```bash
# Levantar el mock server de WireMock (requiere Docker)
docker compose up -d

# Verificar endpoints
curl -i http://localhost:3001/users/1      # 200 + JSON de usuario
curl -i http://localhost:3001/users/99999  # 404 + body de error
curl -i -X POST http://localhost:3001/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane","email":"jane@example.com","role":"user"}'   # 201 tras ~100 ms
curl -i -H "X-Simulate-Latency: 5000" http://localhost:3001/users # 200 tras ~5 s

# Parar
docker compose down
```

Para MSW, importa `msw/handlers.js` en tu setup de tests y arranca el worker/server (`setupWorker` en navegador, `setupServer` en Node — ver documentación de `msw` 2.x).

## Requisitos

- Docker Desktop (imagen WireMock 3.13.2)
- `msw` 2.x para los handlers de frontend
