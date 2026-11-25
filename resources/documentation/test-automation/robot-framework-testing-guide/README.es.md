# Guía de Robot Framework Testing — Companion

> Repositorio companion de la [Guía de Robot Framework Testing para Automatización](https://qapractices.com/es/documentation/robot-framework-testing-guide) en QAPractices.com.

## Qué contiene

- **`tests/login_tests.robot`** — primera suite con SeleniumLibrary: login válido/inválido y user keywords (Pasos 1 y 3).
- **`tests/data_driven_tests.robot`** — ejemplo de `Test Template`: una keyword alimentada por una tabla de datos (Paso 5).
- **`tests/api_tests.robot`** — checks de API a través de la librería Python propia (Paso 7).
- **`resources/common_keywords.robot`** — keywords compartidas: setup/teardown de navegador, login, verificación, screenshot en fallo (Paso 4).
- **`libraries/CustomLibrary.py`** — librería Python que expone `get_api_response`, `post_api_data` y `validate_json_field` como keywords (Paso 7).
- **`.github/workflows/robot-tests.yml`** — workflow de GitHub Actions: versiones fijadas, instalación de Chrome, ejecución por tags y subida de artefactos en fallo (Paso 9).

## Stack

| Herramienta | Versión |
| --- | --- |
| Robot Framework | 7.2.2 |
| SeleniumLibrary | 6.6.1 |
| Python | 3.10+ |
| webdriver-manager | última |

## Uso

```bash
pip install robotframework==7.2.2 robotframework-seleniumlibrary==6.6.1 requests webdriver-manager

# Ejecutar una suite
robot tests/login_tests.robot

# Ejecutar por tag
robot --include smoke tests/
```

Reemplaza los placeholders de `example.com` con la URL de tu aplicación y ajusta los IDs de elementos a tu app. Los reportes se generan en `report.html`, `log.html` y `output.xml`.
