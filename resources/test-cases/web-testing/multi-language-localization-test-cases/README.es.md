# Testing Multi-Idioma y Localización — Companion

Recurso companion de [Casos de Prueba de Multi-Idioma y Localización](https://qapractices.com/es/test-cases/multi-language-localization-test-cases/).

## Contenido

- `mock_server.py` — API i18n stdlib que sirve productos por locale en `en`, `es`, `de`, `ja`, `ar` más un endpoint de pluralización del carrito. El locale `fr` intencionalmente trae una clave faltante (`cta`) y un valor vacío (`description`) para ejercitar el fallback.
- `tests/conftest.py` — levanta el mock en un puerto efímero por sesión de tests.
- `tests/test_localization.py` — subconjunto ejecutable de los casos límite: cambio de locale, fallback por `Accept-Language`, claves faltantes/vacías, formato de moneda, flags RTL y categorías plurales CLDR (en/es/de/ja/ru/ar).
- `requirements.txt` — pytest 8.3 + requests.

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
cd resources/test-cases/web-testing/multi-language-localization-test-cases
pytest tests/ -v
```

Corré el mock de forma standalone para pruebas manuales:

```bash
python mock_server.py 8571
curl "http://127.0.0.1:8571/api/v1/products/PROD-1001?locale=ja-JP"
curl "http://127.0.0.1:8571/api/v1/products/PROD-1001?locale=fr"      # demo de fallback
curl "http://127.0.0.1:8571/api/v1/cart/count?n=5&locale=ru"          # 5 товаров
```

## Qué cubre

- Cambio de locale (`en`/`es`/`de`/`ja`/`ar`) y fallback por `Accept-Language`.
- Clave de traducción faltante y valor vacío → fallback limpio, sin claves raw.
- Formato de moneda por locale (separadores JPY vs EUR).
- Flag RTL (`dir`) para árabe.
- Categorías plurales CLDR incluyendo ruso `one/few/many` y árabe `zero/one/two/few/many`.
