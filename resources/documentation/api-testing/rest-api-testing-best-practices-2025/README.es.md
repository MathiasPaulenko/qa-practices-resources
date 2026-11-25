# Mejores Prácticas de Pruebas de API REST 2025 — Companion

Colección `.http` ejecutable que cubre las áreas de riesgo de la guía: límites de autenticación, límites de paginación, headers de rate-limit, reintentos idempotentes y validación de schema.

## Uso

1. Copia los valores en un archivo `.env` (o el entorno de tu cliente HTTP):

```
API_BASE_URL=https://staging.tu-app.com/api
API_TOKEN=tu-token-de-staging
```

2. Abre `http/api-checks.http` con la extensión REST Client de VS Code, el HTTP Client de JetBrains, o ejecútalo en modo headless con `httpyac`.

3. Cada request documenta el status/aserción esperada en su comentario.

## Checks incluidos

- Health check (200, tiempo de respuesta)
- Request sin autenticación (401)
- Request paginado (200 + campos de paginación)
- Rechazo de página sobredimensionada (400 / clamped)
- Prohibido por rol (403)
- Headers de rate-limit y 429 + Retry-After
- POST idempotente con `Idempotency-Key` (sin duplicados al reintentar)
- Rechazo de body malformado (400)
- Body de error estructurado (sin páginas de error HTML)

Guía completa: https://qapractices.com/es/documentation/rest-api-testing-best-practices-2025
