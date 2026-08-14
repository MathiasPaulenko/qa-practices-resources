# Ejemplo de behave-lint

Proyecto companion de la [Guía de Behave Lint](https://qapractices.com/es/documentation/behave-lint-guide/).

Esta carpeta contiene un `auth.feature` deliberadamente desordenado para que puedas ejecutar `behave-lint` 2.4.1 y ver diagnósticos reales: nombres de escenarios duplicados, tags con casing mixto, fechas hardcodeadas, puntuación final en steps y un secreto hardcodeado.

## Inicio rápido

```bash
cd lint-example
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate en Windows
pip install -r requirements.txt
behave-lint features/
```

La primera ejecución debería reportar 20 diagnósticos (1 error, 8 warnings, 11 info). Luego probá `behave-lint --fix --unsafe-fixes features/` para ver qué problemas son auto-fixeables.

## Archivos

- `features/auth.feature` — archivo Gherkin intencionalmente roto usado en la guía.
- `pyproject.toml` — configuración de `behave-lint` con selección de reglas y overrides.
- `requirements.txt` — fija `behave-lint==2.4.1`.
