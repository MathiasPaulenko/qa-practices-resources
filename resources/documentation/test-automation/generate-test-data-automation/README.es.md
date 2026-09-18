# Cómo Generar Datos de Prueba para Automatización — Companion

Companion ejecutable de la guía
[Cómo Generar Datos de Prueba para Automatización](https://qapractices.com/es/documentation/generate-test-data-automation).

Tres ejemplos autocontenidos que cubren los pasos de la guía — sin servicios externos.

## Contenido

| Carpeta | Stack | Qué cubre |
|--------|-------|-----------|
| `javascript/` | @faker-js/faker 10.6.0 + Jest 30 | Pasos 1, 3, 6-7: básicos de Faker, patrón factory, seeds deterministas, salida CSV/JSON |
| `python/` | faker 40.39.0 + pytest 8.4 | Pasos 2, 5-6: Faker Python, fixture de seeding (sqlite), generación CSV |
| `java/` | Solo JDK (sin dependencias) | Paso 4: `UserBuilder` fluido con aserciones en `main` |

## Ejecutar

```bash
# JavaScript (instala deps, luego corre Jest + los generadores de archivos)
cd javascript && npm ci && npm test && npm run generate

# Python
cd python && pip install -r requirements.txt && pytest -v

# Java
cd java && javac UserBuilder.java && java UserBuilder
```

## Notas

- `faker.seed(12345)` hace determinista cada ejecución — los mismos valores en CI y en local.
- El ejemplo de seeding en Python usa sqlite vía `tmp_path`, así que demuestra el patrón
  real de fixture con `yield` sin necesitar una base de datos corriendo.
- `generate.js` escribe `test-data.json` y `test_users.csv` junto a sí mismo; ambos están en gitignore.

Companion de <https://qapractices.com/es/documentation/generate-test-data-automation>
