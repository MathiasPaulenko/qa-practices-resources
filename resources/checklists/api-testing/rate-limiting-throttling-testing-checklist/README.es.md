# Checklist de Rate Limiting y Throttling — Companion

Scripts ejecutables para el [Checklist de Rate Limiting y Throttling](https://qapractices.com/es/checklists/rate-limiting-throttling-testing-checklist/) de QAPractices.

## Scripts

### `scripts/provoke-429.sh`

Hace bursts contra un endpoint hasta que rechaza, y reporta **qué pedido chocó con la pared**. El borde es lo que importa — el pedido N pasando y el N+1 recibiendo 429 es la verificación de off-by-one que la mayoría de los rate limiters falla. Falla ante cualquier 5xx (el limiter debe rechazar, no romperse) y ante bursts sin 429.

```bash
./scripts/provoke-429.sh https://api.acme-corp.test/search 30
```

### `scripts/verify-rate-limit-headers.sh`

Agota el límite y después inspecciona la respuesta rechazada buscando `Retry-After` y el trío `X-RateLimit-*`. Un 429 sin `Retry-After` deja a los clientes golpeando a ciegas — falla hasta que los cuatro headers aparecen.

```bash
./scripts/verify-rate-limit-headers.sh https://api.acme-corp.test/search 30
```

## Requisitos

- `bash`, `curl`

## Códigos de salida

| Código | Significado |
|--------|-------------|
| 0 | Las verificaciones pasan |
| 1 | Error de uso o endpoint inalcanzable |
| 2 | Verificación falló — sin 429, 5xx en lugar de 429, o headers faltantes |
