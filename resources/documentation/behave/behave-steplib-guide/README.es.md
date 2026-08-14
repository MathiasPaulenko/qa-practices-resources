# Ejemplo de behave-steplib

Ejemplo ejecutable para la [Guía de behave-steplib](https://qapractices.com/es/documentation/behave-steplib-guide/).

## Qué es esto

Un proyecto mínimo de Behave que usa `behave-steplib` 1.5.1 para ejecutar
escenarios de API, datos e IO sin escribir step definitions propios.

## Requisitos

- Python 3.11+
- `behave-steplib[api,io,data]` 1.5.1
- `behave` 1.3.3

## Instalación

```bash
cd api-example
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Si la versión 1.5.1 aún no está en PyPI, usa la rama main de GitHub:

```bash
pip install "git+https://github.com/MathiasPaulenko/behave-steplib.git@main#egg=behave-steplib[api,io,data]"
```

## Ejecución

```bash
behave
```

Deberías ver tres features pasando: API, datos e IO.
