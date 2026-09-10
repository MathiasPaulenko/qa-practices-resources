# API Caching & ETag Guide — Companion

Este companion provee archivos ejecutables para la guía [Guía de Caching y ETag de API](https://qapractices.com/es/documentation/api-caching-etag-testing-guide).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `tests/test_caching_etag.py` | Test de Python requests para ETag match, mismatch y mutación |
| `tests/k6_cache_hit_ratio.js` | Test de carga k6 para cache hit ratio con thresholds |
| `scripts/etag_conditional.sh` | Script de curl para requests condicionales con ETag y Last-Modified |
| `scripts/cdn_validation.sh` | Script de curl para validación de caché de CDN |

## Inicio Rápido

```bash
# Correr tests de Python
pip install requests pytest
pytest tests/test_caching_etag.py -v

# Correr test de carga k6
k6 run tests/k6_cache_hit_ratio.js

# Correr scripts de curl
bash scripts/etag_conditional.sh
bash scripts/cdn_validation.sh
```

## Integración CI

Los tests de Python pueden correr en GitHub Actions con `pytest`. El script de k6 puede correr en CI con `k6 run`.