# Test Automation Framework — Scaffold Mínimo con Playwright

> Recurso companion de [Cómo Construir un Framework de Test Automation desde Cero](https://qapractices.com/es/documentation/test-automation-framework) en QAPractices.com.

Scaffold mínimo en Python/Playwright 1.48 que muestra arquitectura por capas: config, page objects y tests base. Diseñado como punto de partida para equipos que construyen su primera capa de automatización custom.

## Requisitos

- Python 3.12+
- pytest 8.3
- pytest-playwright 0.5
- playwright 1.48

## Setup

```bash
# Clonar e instalar
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install pytest==8.3 pytest-playwright==0.5
playwright install chromium

# Correr tests
pytest --numprocesses 4
```

## Estructura de Proyecto

```text
tests/
  core/
    config.py          # Configuración de ambiente
  ui/
    pages/
      login_page.py    # Page object para login
    specs/
      test_login.py    # Especificaciones de test de login
pyproject.toml         # Configuración de pytest
```

## Archivos

| Archivo | Propósito |
| --------- | ----------- |
| `tests/core/config.py` | URL base, browser, modo headless desde variables de ambiente |
| `tests/ui/pages/login_page.py` | Page object con métodos `open`, `login`, `error_message` |
| `tests/ui/specs/test_login.py` | Casos de test de login válido e inválido |
| `pyproject.toml` | Config de pytest con `--numprocesses 4` para ejecución paralela |

## Arquitectura

El scaffold sigue un diseño de tres capas:

1. **Capa de test** (`tests/ui/specs/`) — lee como una especificación, sin importar browser drivers directamente.
2. **Business layer** (`tests/ui/pages/`) — page objects que encapsulan interacciones de UI.
3. **Core layer** (`tests/core/`) — infraestructura compartida: config, logging, datos de test.

## Licencia

MIT — libre de usar, modificar y distribuir.
