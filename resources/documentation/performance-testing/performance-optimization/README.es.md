# Optimización de Rendimiento — Companion

Archivos companion para la [Guía de Optimización de Rendimiento](https://qapractices.com/es/documentation/performance-optimization).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `src/cursor_pagination.py` | Helper de paginación por cursor: cursor en base64, O(limit) a cualquier profundidad. |
| `src/n_plus_one.py` | Anti-patrón N+1 de ORM vs `prefetch_related` (Django, ilustrativo). |
| `sql/index-optimization.sql` | Patrones de índices PostgreSQL por escenario + EXPLAIN ANALYZE + consulta de índices sin uso. |
| `redis/cache-invalidation.md` | Comandos Redis de caché: TTL, invalidación por tags, notas de calentamiento. |
| `nginx/gzip.conf` | Compresión de respuestas para APIs JSON (5-10x en JSON). |
| `tests/test_cursor_pagination.py` | Suite pytest del helper de paginación — solo stdlib, sin base de datos. |

## Requisitos

- Python 3.10+
- pytest 8.3+
- (opcional) Django 5.x para el ejemplo N+1; PostgreSQL para los snippets SQL

## Uso

1. Instala las dependencias: `pip install -r requirements.txt`.
2. Corre `pytest tests/ -v` — verifica la codificación del cursor, la continuidad entre páginas y el comportamiento al final de la lista.
3. Copia los patrones de `sql/index-optimization.sql` a tu tooling de migraciones; corre `EXPLAIN (ANALYZE, BUFFERS)` antes y después de cada índice.
4. Aplica `nginx/gzip.conf` a la configuración nginx de la API.

## Integración en CI

```yaml
- run: pip install -r requirements.txt && pytest tests/ -v --tb=short
```
